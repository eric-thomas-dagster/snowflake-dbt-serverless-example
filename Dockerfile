# Dockerfile for Dagster Cloud serverless deployment

FROM python:3.11-slim

# Set working directory
WORKDIR /opt/dagster/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy the entire project
COPY . .

# Set environment variables for Dagster Cloud
ENV DAGSTER_HOME=/opt/dagster/app

# Dagster Cloud serverless will handle all networking and process management
# No need to expose ports or specify command - Dagster Cloud manages this
