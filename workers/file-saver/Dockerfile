FROM python:3.9-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache file-dev

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create directory for logs
RUN mkdir -p /app/logs && \
    chmod 777 /app/logs

# Set the entrypoint
CMD ["python", "-m", "handler"]