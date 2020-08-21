import os
import json
import random
import time
import datetime
import logging
import traceback
import boto3

# selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# set up Logger
import logging
import sys
logger = logging.getLogger()
for h in logger.handlers:
    logger.removeHandler(h)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(levelname)s %(asctime)s [%(funcName)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)


def set_selenium_options():
    """ Set selenium options """
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--window-size=1280,1024')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--homedir=/tmp")

    return webdriver.Chrome('/opt/chromedriver', chrome_options=options)


def wait_until_element_present(driver, key, location):
    """ Wait until element is presented at location """
    elm = None
    counter = 4
    timeup = 20
    while counter < timeup:
        try:
            elm = WebDriverWait(driver, counter).until(
                EC.presence_of_element_located((key, location)))
        except NoSuchElementException as e:
            logger.warn("[WARN] {e}".format(e=e))
            logger.warn("counter: {val}".format(val=counter))
            counter += 2
            continue
        except TimeoutException as e:
            logger.warn("[WARN] {e}".format(e=e))
            logger.warn("counter: {val}".format(val=counter))
            counter += 2
            continue
        else:
            break
    
    return elm

def get_text_by_xpath(driver, location):
    return driver.find_element_by_xpath(location).text


def save_screenshot(driver, filename):
    """ Save screenshot at Amazon S3 """
    s3client = boto3.client('s3')
    driver.save_screenshot("/tmp/" + filename)
    bucket = os.environ.get("S3BUCKET", "")
    s3client.upload_file(
        Filename="/tmp/" + filename,
        Bucket=bucket,
        Key=filename
    )
    return


def terminate_driver(driver):
    """ Terminate driver """
    driver.close()
    driver.quit()
    return


def main(event, context):
    """ Entrypoint of lambda """

    # Debug event to CloudWatch log
    starttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info("starttime: {}".format(starttime))
    logging.info(json.dumps(event))

    driver = None
    target = None
    url = "https://gkzz.github.io"
    location = '//*[@id="featured"]/article/ul[1]/li[2]/p'

    try:        
        driver = set_selenium_options()
        driver.maximize_window()
        driver.get(url)
        presented = wait_until_element_present(
            driver, By.XPATH, location)
        save_screenshot(
            driver, 'ss_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S' + '.png'))
        if presented is not None:
            target = driver.find_element_by_xpath(location).text

        endtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info("endtime: {}".format(endtime))
        terminate_driver(driver)
        return {
            "statusCode": 200,
            "body": target
        }
    except Exception as e:
        logger.error("[ERROR] {e}".format(e=e))
        terminate_driver(driver)
        return {
            "statusCode": 400,
            "body": e
        }
