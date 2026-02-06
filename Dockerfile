# Use official Python slim image
FROM python:3.11-slim

# Install system dependencies for MariaDB and build tools
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install system dependencies for MariaDB/MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*


# Copy requirements
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy all project files into container
COPY . .

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

