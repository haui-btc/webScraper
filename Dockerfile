# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# install apt-utils
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

# install wget and gnupg and curl
RUN apt-get update && apt-get install -y wget gnupg curl

# Install Chromium and related packages
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y chromium

# Install the required dependencies for Pyppeteer
RUN apt-get install -y libx11-xcb1 libxcomposite1 libxdamage1 libxi6 libxtst6 libnss3 libcups2 libxss1 libxrandr2 libasound2 libpangocairo-1.0-0 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0

RUN python3 --version
RUN pip3 --version

RUN pip install --no-cache-dir --upgrade pip

# Install pip requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . /app

# Set environment variable for Chrome to run in headless mode
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/lib/google-chrome

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "app/monitor.py"]
