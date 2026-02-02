FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Explicitly check if uvicorn is installed during the build
# This will cause the build to fail early if uvicorn is missing
RUN python -m uvicorn --version

# Copy the entire project
COPY . .

# Expose the port
EXPOSE 8000

# Using the full path to the python executable and the module flag
CMD ["python3", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]