# Guestbook Web Application Deployment with Docker Stack

This project demonstrates how to deploy a simple Go-based guestbook web application on a VPS using Docker Stack with Docker Swarm mode. The application tracks website visits and displays motivational quotes, utilizing a PostgreSQL database. This README provides an overview of the setup, deployment process, and automation using GitHub Actions for CI/CD.

## Prerequisites

- **VPS**: A virtual private server (e.g., Hostinger KVM 2 or higher) with Ubuntu 24.04 installed.
- **Docker**: Docker Engine installed on the VPS.
- **Domain Name** (optional): A domain name with an A record pointing to the VPS (e.g., `zenful.site`).
- **GitHub Repository**: A repository containing the application code, Dockerfile, and Docker Stack configuration.
- **SSH Key Pair**: For secure remote access and deployment.
- **GitHub Actions**: For automated testing, building, and deployment.

## Project Structure

- `Dockerfile`: Defines the Docker image for the Go-based guestbook web application.
- `docker-stack.yml`: Defines the application stack, including the web application and PostgreSQL database services.
- `.github/workflows/deploy.yml`: GitHub Actions workflow for testing, building, and deploying the application.

## Setup Instructions

### 1. VPS Setup
1. **Provision a VPS**: Use a provider like Hostinger to set up a VPS (e.g., KVM 2 with 2 vCPUs, 8GB RAM, 100GB SSD).
2. **Secure the VPS**:
   - Set a strong password for the root user.
   - Configure SSH public key authentication.
   - (Optional) Harden SSH, add a non-root user, and enable a firewall (refer to the production-ready VPS guide linked in the video description).
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
   Save the generated token for potential future clustering (not covered in this guide).

### 3. Configure Docker Context for Remote Management
1. Create a Docker context to manage the VPS remotely:
   ```bash
   docker context create zenful-vps --docker "host=ssh://root@zenful.site"
   ```
   Replace `zenful.site` with your VPS IP or domain.
2. Switch to the new context:
   ```bash
   docker context use zenful-vps
   ```

### 4. Deploy the Application
1. **Update `docker-stack.yml`**:
   - The file defines two services: `web` (the Go application) and `db` (PostgreSQL).
   - Example configuration:
     ```yaml
     version: '3.8'
     services:
       web:
         image: ghcr.io/username/guestbook:${GIT_COMMIT_HASH:-latest}
         ports:
           - "80:8080"
         environment:
           - DB_PASSWORD_FILE=/run/secrets/db-password
         secrets:
           - db-password
         deploy:
           update_config:
             order: start-first
       db:
         image: postgres:13
         environment:
           - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
         secrets:
           - db-password
     secrets:
       db-password:
         external: true
     ```
2. **Create a Docker Secret**:
   ```bash
   printf "your_secure_password" | docker secret create db-password -
   ```
3. **Deploy the Stack**:
   ```bash
   docker stack deploy -c docker-stack.yml zenful-stack
   ```
4. **Verify Deployment**:
   ```bash
   docker stack services zenful-stack
   ```
   Visit `http://zenful.site` to confirm the application is running.

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
   Example `deploy.yml`:
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
         - name: Run Tests
           run: go test ./...
     build-and-push:
       needs: test
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Log in to GitHub Container Registry
           run: echo "${{ secrets.GHCR_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
         - name: Build and Push Docker Image
           run: |
             docker build -t ghcr.io/username/guestbook:${{ github.sha }} -t ghcr.io/username/guestbook:latest .
             docker push ghcr.io/username/guestbook:${{ github.sha }}
             docker push ghcr.io/username/guestbook:latest
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
             stack: zenful-stack
             file: docker-stack.yml
             host: ssh://deploy@zenful.site
             user: deploy
             ssh-private-key: ${{ secrets.DEPLOY_SSH_PRIVATE_KEY }}
             env-file: .env
   ```
6. **Push Changes**:
   Commit and push changes to the `main` branch to trigger the pipeline.

### 6. Additional Features
- **Rolling Updates**: Configured in `docker-stack.yml` with `deploy.update_config.order: start-first` for zero-downtime deployments.
- **Service Rollbacks**:
   ```bash
   docker service rollback zenful-stack_web
   ```
- **Load Balancing**: Docker Swarm provides built-in load balancing. Scale services:
   ```bash
   docker service scale zenful-stack_web=3
   ```
   View logs to confirm round-robin distribution:
   ```bash
   docker service logs -f zenful-stack_web
   ```
- **Traefik for HTTPS**: Optionally, add Traefik for load balancing and automatic SSL:
   ```yaml
   services:
     traefik:
       image: traefik:v2.10
       ports:
         - "80:80"
         - "443:443"
       command:
         - "--api.insecure=true"
         - "--providers.docker=true"
         - "--entrypoints.web.address=:80"
         - "--entrypoints.websecure.address=:443"
       volumes:
         - /var/run/docker.sock:/var/run/docker.sock
   ```

## Troubleshooting
- **Secret Path Issues**: Ensure secrets are defined as `external` in `docker-stack.yml` and created on the VPS.
- **Deployment Failures**: Check logs (`docker service logs zenful-stack_web`) for errors, such as incorrect image tags or missing environment variables.
- **Client IP Forwarding**: Use Traefik or the Docker Ingress Routing Daemon for accurate client IP forwarding.

## Resources
- [Docker Documentation](https://docs.docker.com)
- [Hostinger VPS](https://hostinger.com/dreams-of-code) (Use coupon code `dreams-of-code` for a discount)
- [GitHub Repository](https://github.com/username/guestbook)
- [Production-Ready VPS Guide](https://example.com/production-vps-guide)

## Acknowledgments
- Thanks to Hostinger for sponsoring the VPS instance used in this project.
- Coupon code: `dreams-of-code` for additional discounts on Hostinger VPS plans.
