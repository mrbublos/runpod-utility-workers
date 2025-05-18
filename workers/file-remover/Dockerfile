FROM python:3.10-slim

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup --system app && adduser --system --group app

# Copy the application code with ownership set to the non-root user
COPY --chown=app:app handler.py schema.py .

# Switch to the non-root user
USER app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV USER_DATA_FOLDER=/user_data

# Set entrypoint
CMD ["python", "-u", "handler.py"]