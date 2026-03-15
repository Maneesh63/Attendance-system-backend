FROM python:3.12-slim

WORKDIR /app

# Install OS dependencies for Django + mysqlclient
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    default-mysql-client \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

EXPOSE 8000

# Default command (can override on Render)
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1"]