FROM python:3.11.7-slim-bookworm

# Prevents Python from writing .pyc files and enables immediate log output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Default command (can be overridden by docker-compose)
CMD ["python", "package_statistics.py", "amd64"]
