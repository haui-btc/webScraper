# Use the official Python 3.11-slim-buster image as the base image
FROM python:3.11-slim-buster

# Run pip install --upgrade pip
RUN pip install --upgrade pip

# Set the working directory to /app
WORKDIR /app
# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire src directory to the container's /app directory
COPY ./app ./app

# Start the monitor.py file with python3
CMD ["python3", "./monitor.py"]

