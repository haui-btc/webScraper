# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Upgrade to latest pip version
RUN pip install --upgrade pip

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./src/ /app/

# Run the command to start the server
CMD ["python3", "./monitor.py"]
