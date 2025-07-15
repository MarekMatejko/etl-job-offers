# Use a minimal Python 3.11 image as the base
FROM python:3.11-slim

# Install system dependencies:
# - libpq-dev: required for psycopg2 PostgreSQL client
# - wget, curl, unzip: to download and unpack ChromeDriver
# - chromium: headless browser for scraping
RUN apt-get update && apt-get install -y \
    libpq-dev \
    wget \
    curl \
    unzip \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Download a specific version of ChromeDriver and install it to /usr/local/bin
RUN wget -q "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application code into the container
COPY . .


# Optional default command (disabled for now, can be overridden by docker-compose)
#CMD ["python", "scraping_script.py"]

