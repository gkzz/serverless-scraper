#!/bin/bash

set -e

#CHROMEVERSION="v1.0.0-45"
#DRIVERVERSION="2.40"

CHROMEVERSION="v1.0.0-50"
DRIVERVERSION="2.41"

CHROMEFILE=https://github.com/adieuadieu/serverless-chrome/releases/download/${CHROMEVERSION}/stable-headless-chromium-amazonlinux-2017-03.zip
CHROMEDRIVER=https://chromedriver.storage.googleapis.com/${DRIVERVERSION}/chromedriver_linux64.zip

curl -SL $CHROMEFILE > headless-chromium.zip
unzip headless-chromium.zip 
rm headless-chromium.zip

curl -SL $CHROMEDRIVER > chromedriver.zip
unzip chromedriver.zip 
rm -rf chromedriver.zip

mv chromedriver headless-chromium selenium-layer/driver/
