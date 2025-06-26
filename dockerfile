FROM python:3.10-slim

RUN apt-get update && apt-get install -y wget curl unzip gnupg2

# Install Google Chrome stable
RUN wget -O chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./chrome.deb \
    && rm chrome.deb

# Set ChromeDriver version to match Chrome version
ENV CHROMEDRIVER_VERSION=114.0.5735.90

# Download ChromeDriver and unzip it
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip

RUN google-chrome --version


# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app files
COPY . /app
WORKDIR /app

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
