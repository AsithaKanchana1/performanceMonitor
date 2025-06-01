# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY performance_monitor.py .

# Define environment variables for configuration (optional, can be overridden at runtime)
ENV LOG_INTERVAL_SECONDS=5
ENV LOG_FILE_NAME=system_performance.csv
ENV LOG_DIRECTORY=performance_logs

# Ensure the log directory exists (will be created inside the container if not mounted)
# And set permissions if necessary, though Python's os.makedirs should handle it.
# RUN mkdir -p /app/${LOG_DIRECTORY}

# Command to run the application
CMD ["python", "./performance_monitor.py"]