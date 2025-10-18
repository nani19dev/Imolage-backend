# Django Web Application Deployment with Docker Stack

This project demonstrates how to deploy a Django-based web application on a VPS using Docker Stack with Docker Swarm mode. The application is served with Traefik for load balancing and HTTPS support, and automated deployments are configured using GitHub Actions for CI/CD. The setup ensures scalability, zero-downtime deployments, and secure secret management.

## Prerequisites

- **VPS**: A virtual private server (e.g., Hostinger KVM 2 or higher) with Ubuntu 24.04 installed.
- **Docker**: Docker Engine installed on the VPS.
- **Domain Name**: A domain name with A records pointing to the VPS (e.g., `backendvps.eu` for the app, `traefik.backendvps.eu` for the Traefik dashboard).
- **GitHub Repository**: A repository containing the Django application code, Dockerfile, and Docker Stack configuration.
- **SSH Key Pair**: For secure remote access and deployment.
- **GitHub Actions**: For automated testing, building, and deployment.

## Project Structure

- `Dockerfile`: Defines the Docker image for the Django application.
- `docker-stack.yml`: Defines the application stack, including the Django application and Traefik services.
- `.github/workflows/deploy.yml`: GitHub Actions workflow for testing, building, and deploying the application.

## Setup Instructions

### 1. VPS Setup
1. **Provision a VPS**: Use a provider like Hostinger to set up a VPS (e.g., KVM 2 with 2 vCPUs, 8GB RAM, 100GB SSD).
2. **Secure the VPS**:
   - Set a strong password for the root user.
   - Configure SSH public key authentication.
   - Harden SSH, add a non-root user, and enable a firewall (refer to a production-ready VPS guide for details).
3. **Install Docker**:
   ```bash
   # Add Docker to APT sources
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

   # Install Docker Engine
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io
   ```
4. **Verify Docker Installation**:
   ```bash
   docker ps
   ```

### 2. Enable Docker Swarm Mode
1. Initialize Docker Swarm on the VPS:
   ```bash
   docker swarm init
   ```
   Save the generated token for potential future clustering.

### 3. Configure Docker Context for Remote Management
1. Create a Docker context to manage the VPS remotely:
   ```bash
   docker context create django-vps --docker "host=ssh://root@backendvps.eu"
   ```
   Replace `backendvps.eu` with your VPS IP or domain.
2. Switch to the new context:
   ```bash
   docker context use django-vps
   ```

### 4. Deploy the Application
1. **Update `docker-stack.yml`**:
   The provided `docker-stack.yml` defines two services: `django-app` (the Django application) and `traefik` (for load balancing and HTTPS).
   ```yaml
   version: '3.8'
   services:
     django-app:
       build:
         context: .
         dockerfile: Dockerfile
       deploy:
         replicas: 2 # Scale for production
         labels:
           - "traefik.enable=true"
           - "traefik.http.routers.django.rule=Host(`backendvps.eu`)" # Replace with your production domain
           - "traefik.http.services.django.loadbalancer.server.port=8000"
           - "traefik.http.routers.django.entrypoints=web"
           - "traefik.http.routers.django.tls.certresolver=myresolver" # Enable HTTPS
       environment:
         - DOMAIN=backendvps.eu # Replace with your production domain
         # - SECRET_KEY_VALUE=${SECRET_KEY_VALUE}
         # - DB_HOST=${DB_HOST}
         # - DB_NAME=${DB_NAME}
         # - DB_USER=${DB_USER}
         # - DB_PORT=${DB_PORT}
         # - DB_PWD=${DB_PWD}
       networks:
         - web
     traefik:
       image: traefik:v2.10
       command:
         - "--api.insecure=false" # Disable insecure API in production
         - "--providers.docker=true"
         - "--providers.docker.swarmMode=true" # Enable Swarm mode
         - "--entrypoints.web.address=:80"
         - "--entrypoints.websecure.address=:443" # Enable HTTPS
         - "--certificatesresolvers.myresolver.acme.tlschallenge=true" # Enable Let's Encrypt
         - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
       ports:
         - "80:80"
         - "443:443" # Enable HTTPS
       networks:
         - web
       volumes:
         - /var/run/docker.sock:/var/run/docker.sock:ro
         - ./letsencrypt:/letsencrypt
       deploy:
         placement:
           constraints: [node.role == manager] # Run on manager node
       labels:
         - "traefik.enable=true"
         - "traefik.http.routers.traefik.rule=Host(`traefik.backendvps.eu`)" # Replace with your Traefik dashboard domain
         - "traefik.http.routers.traefik.service=api@internal"
         - "traefik.http.routers.traefik.entrypoints=websecure" # Use HTTPS for dashboard
         - "traefik.http.routers.traefik.tls.certresolver=myresolver"
   networks:
     web:
       driver: overlay # Use overlay network for Swarm
   ```
2. **Create Docker Secrets** (if needed):
   For sensitive environment variables like `SECRET_KEY_VALUE`, `DB_PWD`, etc., create Docker secrets:
   ```bash
   printf "your_secret_key" | docker secret create django_secret_key -
   printf "your_db_password" | docker secret create db_password -
   ```
   Update `docker-stack.yml` to reference secrets:
   ```yaml
   services:
     django-app:
       environment:
         - SECRET_KEY_VALUE=/run/secrets/django_secret_key
         - DB_PWD=/run/secrets/db_password
       secrets:
         - django_secret_key
         - db_password
     db:
       environment:
         - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
       secrets:
         - db_password
   secrets:
     django_secret_key:
       external: true
     db_password:
       external: true
   ```
3. **Deploy the Stack**:
   ```bash
   docker stack deploy -c docker-stack.yml django-stack
   ```
4. **Verify Deployment**:
   ```bash
   docker stack services django-stack
   ```
   Visit `https://backendvps.eu` to confirm the application is running.

### 5. Set Up Automated Deployments with GitHub Actions
1. **Create a Deployment User**:
   ```bash
   sudo adduser deploy
   sudo usermod -aG docker deploy
   ```
2. **Generate SSH Key Pair** (on your local machine):
   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/deploy_key
   ```
3. **Add Public Key to VPS**:
   ```bash
   su - deploy
   mkdir ~/.ssh
   echo "<public_key_content>" > ~/.ssh/authorized_keys
   ```
   Restrict the key to only allow `docker stack deploy`:
   ```bash
   echo 'command="docker stack deploy",no-pty,no-port-forwarding <public_key_content>' > ~/.ssh/authorized_keys
   ```
4. **Add Private Key to GitHub Secrets**:
   - Navigate to your GitHub repository > Settings > Secrets and variables > Actions > New repository secret.
   - Add the private key as `DEPLOY_SSH_PRIVATE_KEY`.
5. **Configure GitHub Actions Workflow**:
   Example `.github/workflows/deploy.yml`:
   ```yaml
   name: CI/CD Pipeline
   on:
     push:
       branches:
         - main
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.10'
         - name: Install Dependencies
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt
         - name: Run Tests
           run: python manage.py test
     build-and-push:
       needs: test
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Log in to GitHub Container Registry
           run: echo "${{ secrets.GHCR_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
         - name: Build and Push Docker Image
           run: |
             docker build -t ghcr.io/username/django-app:${{ github.sha }} -t ghcr.io/username/django-app:latest .
             docker push ghcr.io/username/django-app:${{ github.sha }}
             docker push ghcr.io/username/django-app:latest
     deploy:
       needs: build-and-push
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Create Env File
           run: echo "GIT_COMMIT_HASH=${{ github.sha }}" > .env
         - name: Deploy Docker Stack
           uses: docker-deploy-action@v1
           with:
             stack: django-stack
             file: docker-stack.yml
             host: ssh://deploy@backendvps.eu
             user: deploy
             ssh-private-key: ${{ secrets.DEPLOY_SSH_PRIVATE_KEY }}
             env-file: .env
   ```
6. **Push Changes**:
   Commit and push changes to the `main` branch to trigger the pipeline.

### 6. Additional Features
- **Rolling Updates**: Configured with `deploy.update_config.order: start-first` for zero-downtime deployments (add to `django-app` service if needed).
- **Service Rollbacks**:
   ```bash
   docker service rollback django-stack_django-app
   ```
- **Load Balancing**: Traefik provides load balancing across replicas, configured with labels in `docker-stack.yml`.
- **HTTPS Support**: Traefik automatically handles SSL certificates via Let's Encrypt.
- **Scaling**:
   ```bash
   docker service scale django-stack_django-app=3
   ```
   View logs to confirm load balancing:
   ```bash
   docker service logs -f django-stack_django-app
   ```

## Troubleshooting
- **Secret Path Issues**: Ensure secrets are defined as `external` and created on the VPS.
- **Deployment Failures**: Check logs (`docker service logs django-stack_django-app`) for errors, such as incorrect image tags or missing environment variables.
- **Traefik Issues**: Verify domain configurations and ensure A records point to the VPS IP.
- **Client IP Forwarding**: Traefik forwards client IPs correctly; ensure proper configuration if issues arise.

## Resources
- [Docker Documentation](https://docs.docker.com)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [GitHub Repository](https://github.com/username/django-app)
- [Hostinger VPS](https://hostinger.com/dreams-of-code) (Use coupon code `dreams-of-code` for a discount)

## Acknowledgments
- Thanks to Hostinger for sponsoring the VPS instance used in this project.
- Coupon code: `dreams-of-code` for additional discounts on Hostinger VPS plans.
