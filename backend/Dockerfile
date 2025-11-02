# ---------- Base Image ----------
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Environment configs (disable .pyc, enable flush)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system deps for PostgreSQL & builds
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend code into container
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
