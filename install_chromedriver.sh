#!/bin/bash

set -e

CHROME_VERSION=$(google-chrome --version | grep -oP '\d+' | head -1)
echo "Detected Chrome major version: $CHROME_VERSION"

DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
echo "Matching ChromeDriver version: $DRIVER_VERSION"

wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip"
unzip /tmp/chromedriver.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
rm /tmp/chromedriver.zip
