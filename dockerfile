FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl unzip wget gnupg2 ca-certificates fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 xdg-utils

# Install Chrome stable
RUN wget -O chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./chrome.deb \
    && rm chrome.deb

# Copy the ChromeDriver installer script and run it
COPY install_chromedriver.sh /tmp/install_chromedriver.sh
RUN chmod +x /tmp/install_chromedriver.sh && /tmp/install_chromedriver.sh

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . /app
WORKDIR /app

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
