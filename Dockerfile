# Use official slim Python image
FROM python:3.12-slim

WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    default-mysql-client \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port for Render
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "root.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]