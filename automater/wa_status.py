"""
change the status of your whatsapp account
usage:
    wa_status.py "<status>" <head>
"""
import argparse
from sys import exit
from env import FFPROFILEPATHW, FFPROFILEPATHL
import logging
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)
logging.basicConfig(filename="db_status.log", encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="change the whatsapp status")
    parser.add_argument("status",type=str, help="your whatsapp status")
    args = parser.parse_args()

    logger.debug('[start]')
    message = args.status
    logger.debug('status -> %s', message)
    if len(message) >= 139:
        print("Message Is Too Long")
        logger.error("status '%s' is logger than 139 characters", message)
        exit(-1)

    FFPROFILEPATH = FFPROFILEPATHW if os.name == "nt" else FFPROFILEPATHL

    # check the docs on how to bypass the whatsapp web login everytime
    # 1. create a new firefox profile; search -> about:profile
    # 2. go to whatsapp and login 
    # 3. enter the path
    options = FirefoxOptions()
    options.add_argument("--headless")
    firefoxprofile = webdriver.FirefoxProfile(FFPROFILEPATH)
    options.profile = firefoxprofile 
    driver = webdriver.Firefox(options=options)
    driver.get("https://web.whatsapp.com/")
    logger.debug("logging in")
    wait = WebDriverWait(driver, 5200)
    wait.until(EC.visibility_of_element_located((
        By.XPATH,
        "/html/body/div[1]/div/div/div[2]/div[3]/header/header/div/div[1]/h1"
    )))
    logger.debug("starting action chain")
    # 1. load the profile and about
    # 2. /html/body/div[1]/div/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[4]/div[2]/div/span[2]/button/span
    actions = ActionChains(driver)
    # CTRL + ALT + P
    actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('p').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
    wait.until(EC.visibility_of_element_located((
        By.CSS_SELECTOR,
        "[title^='Click to edit About']"
    )))
    logger.debug("driver finding element 'edit icon'")
    try:
        driver.find_element(By.CSS_SELECTOR,"[title^='Click to edit About']").click()
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        actions.send_keys(Keys.BACKSPACE).perform()
        actions.send_keys(message).perform()
        actions.send_keys(Keys.ENTER).perform()
        actions.send_keys(Keys.ESCAPE).perform()
    except Exception as e:
        logger.error("Driver Cannot Find The 'EDIT' icon")
    logger.debug('[quit]')
    driver.quit()