FROM python:3.12-slim

# Install system dependencies: Firefox, wget, and required libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        firefox-esr \
        wget \
        ca-certificates \
        fonts-liberation \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libc6 \
        libcairo2 \
        libcups2 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libx11-6 \
        libxcomposite1 \
        libxdamage1 \
        libxext6 \
        libxfixes3 \
        libxrandr2 \
        libxrender1 \
        libxtst6 \
        xdg-utils \
        && rm -rf /var/lib/apt/lists/*

# Download and install Geckodriver
# Download and install Geckodriver (latest compatible version)
ENV GECKODRIVER_VERSION=0.36.0

RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz \
    && tar -xzf geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz



# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script into the container
COPY seldenem2.py .

# Set the entrypoint
CMD ["python", "seldenem2.py"]


####################### TRY a different base image ######################
#FROM selenium/standalone-firefox:latest
#
#USER root
#
## Install Python and pip
#RUN apt-get update && \
#    apt-get install -y python3 python3-pip && \
#    rm -rf /var/lib/apt/lists/*
#
## Copy your script
#COPY seldenem2.py /seldenem2.py
#
## Install Python dependencies if needed
## COPY requirements.txt .
## RUN pip3 install --no-cache-dir -r requirements.txt
#
#CMD ["python3", "/seldenem2.py"]