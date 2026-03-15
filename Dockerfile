FROM python:3.12-slim

WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose (optional)
EXPOSE 8000

# Default command (can be overridden by Render startCommand)
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1"]