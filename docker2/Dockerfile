# Use official Python image with Debian base
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables to use Chrome correctly
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Copy code
WORKDIR /app
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python", "upgrade.py"]
