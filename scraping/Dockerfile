FROM python:3.11-slim


RUN apt-get update && apt-get install -y \
    libpq-dev \
    wget \
    curl \
    unzip \
    chromium \
    && rm -rf /var/lib/apt/lists/*


RUN wget -q "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["python", "scraping_script.py"]