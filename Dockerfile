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

# Copy the production start script and make it executable
COPY scripts/start-prod.sh /app/scripts/start-prod.sh
RUN chmod +x /app/scripts/start-prod.sh

# Create log directory and set permissions so the app can write logs
RUN mkdir -p /var/log/fortuna-flow && chmod 777 /var/log/fortuna-flow

# Set the Python path to include the src directory
ENV PYTHONPATH=/app/src

# Expose port 8000 for the backend API
EXPOSE 8000

# Use the production start script as the container entrypoint
CMD ["/app/scripts/start-prod.sh"]