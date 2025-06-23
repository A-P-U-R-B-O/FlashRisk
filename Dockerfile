FROM python:3.11-slim

# Set environment variables for python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY app ./app

# Expose port for Uvicorn
EXPOSE 10000

# Command to run the backend (FastAPI with Uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
