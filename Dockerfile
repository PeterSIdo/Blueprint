FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
build-essential \
libpq-dev \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
# Install pip dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy rest of the application
COPY . .

# Expose port for Cloud Run
EXPOSE 8080

# Use gunicorn as the production server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "run:app"]