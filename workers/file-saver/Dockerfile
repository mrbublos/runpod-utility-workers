FROM python:3.9-alpine

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy the application code with ownership set to the non-root user
COPY --chown=appuser:appgroup handler.py .

# Switch to the non-root user
USER appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV USER_DATA_FOLDER=/user_data

# Set the entrypoint
CMD ["python", "-m", "handler"]