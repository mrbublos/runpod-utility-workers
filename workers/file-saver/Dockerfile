FROM python:3.10-slim

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code with ownership set to the non-root user
COPY --chown=appuser:appgroup handler.py schema.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV USER_DATA_FOLDER=/user_data

# Set the entrypoint
CMD ["python", "-u", "handler.py"]