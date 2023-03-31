# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /app

# Set build-time proxy environment variables
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

# Set runtime proxy environment variables
ENV http_proxy=$HTTP_PROXY
ENV https_proxy=$HTTPS_PROXY
ENV no_proxy=$NO_PROXY

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./src/app /app/app
COPY ./src/run.py /app/

# Set the environment variable for uvicorn
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the command to start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]




