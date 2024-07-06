# Use Python 3.11.3 as the base image
FROM python:3.11.3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire requirements directory
COPY requirements /app/requirements

# Install production dependencies
RUN pip install --no-cache-dir -r /app/requirements/prod.txt

# Copy the src directory contents into the container at /app/src
COPY src /app/src

# Copy .env file into the container
COPY .env /app/.env

# Set the Python path to include the src directory
ENV PYTHONPATH=/app/src

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application with Gunicorn, using environment variables
CMD gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}