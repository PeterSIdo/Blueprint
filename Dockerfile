FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy rest of the application
COPY . .

# Expose port for Cloud Run
EXPOSE 8080

# Use gunicorn as the production server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]