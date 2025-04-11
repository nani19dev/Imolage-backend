# Stage 1: Base build stage
FROM python:3.12-alpine AS builder

# Set working directory
WORKDIR /app

# Set environment variables 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# Upgrade pip and install dependencies
#RUN pip install --upgrade pip 

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.12-alpine

# Install shadow to get useradd
RUN apk update && apk add shadow
 
RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app
 
# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app
 
# Copy application code
COPY --chown=appuser:appuser . .
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

ARG DOMAIN
ENV DOMAIN=$DOMAIN

ARG DB_ENGIN
ENV DB_ENGIN=$DB_ENGIN

ARG DB_HOST
ENV DB_HOST=$DB_HOST

ARG DB_NAME
ENV DB_NAME=$DB_NAME

ARG DB_USER
ENV DB_USER=$DB_USER

ARG DB_PORT
ENV DB_PORT=$DB_PORT

ARG DB_PWD
ENV DB_PWD=$DB_PWD

ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY
 
# Switch to non-root user
USER appuser

# Copy the project to the container
COPY . /app/

# Run migrations.
#RUN python manage.py makemigrations 
#RUN python manage.py migrate

# Expose the port your Django app runs on
EXPOSE 8000

# Run the Django development server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "backend.wsgi:application"]