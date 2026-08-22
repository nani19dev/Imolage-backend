### Stage 1: Base build stage
FROM python:3.12-alpine AS builder

# Set working directory
WORKDIR /app

# Set environment variables 
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1 
ENV PIP_NO_CACHE_DIR=1

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Build deps needed to compile psycopg2-binary on musl
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

### Stage 2: Production stage
FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Install shadow to get useradd
#RUN apk update && apk add shadow 

# Install shadow to get useradd, libpq for psycopg2 at runtime, curl for the healthcheck
RUN apk update && apk add shadow libpq curl
 
RUN useradd -m -r appuser && \
   chown -R appuser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy requirements.txt to the container
COPY requirements.txt /app/
 
# Copy application code (owned by appuser, not root)
COPY --chown=appuser:appuser . .

#RUN chmod +x entrypoint.sh
  
# Switch to non-root user
USER appuser

# Copy the project to the container
COPY . /app/

# Expose the port your Django app runs on
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
# Run the Django development server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "backend.wsgi:application"]