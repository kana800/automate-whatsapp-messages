"""
send bulk messages through whatsapp

usage:
    wa_bulk.py <content>
example:
    wa_bulk.py "content.json"

bulk messages only accepts a json file
in the following format
{
    'contactname': 'message',
    'contactname': 'message'
}
"""
import argparse
import logging

from os import path
from os import name as osname

import sys
import json
import time

from env import FFPROFILEPATHW, FFPROFILEPATHL, LOGPATH

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)
logpath = path.join(LOGPATH, "db_wa_bulk.log")
logging.basicConfig(filename= logpath, encoding='utf-8', level=logging.INFO)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# contact name is You by default
# will send a message to yourself
contact_name = "You"

def sendMessage(driver:webdriver, to:str, message:str):
    actions = ActionChains(driver)
    # CTRL + ALT + N
    actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('n').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
    actions.send_keys(to).perform()
    body = driver.find_element(By.TAG_NAME, 'body')
    # TODO: add error checking here
    if (body.text.find("No results found")) == -1:
        actions.send_keys(Keys.ENTER).perform()
        actions.send_keys(message)
        actions.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
        actions.send_keys(Keys.ENTER).perform()
        actions.send_keys(Keys.ESCAPE).perform()
        # waiting until whatsapp send the message
        # to its server;
        time.sleep(20)
    else:
        logger.debug("contact name %s cannot be found", to)
        actions.send_keys(Keys.ESCAPE).perform()

if __name__ == "__main__":

    logger.info("[start]")

    parser = argparse.ArgumentParser(description="send bulk whatsapp message")
    parser.add_argument("content", type=str, help="if message; type message or else enter filepath")
    args = parser.parse_args()

#    filename = args.content
#    if (path.exists(filename)):
#        with open(filename, 'r') as f:
#            content = json.load(f)
#    else:
#        logger.info("cannot file: %s", filename)
#        sys.exit(-1)
#
#    # check the docs on how to bypass the whatsapp web login everytime
#    # 1. create a new firefox profile; search -> about:profile
#    # 2. go to whatsapp and login 
#    # 3. enter the path
#    options = FirefoxOptions()
#    options.add_argument("--headless")
#    FFPROFILEPATH = FFPROFILEPATHW if osname == "nt" else FFPROFILEPATHL
#
#    firefoxprofile = webdriver.FirefoxProfile(FFPROFILEPATH)
#    options.profile = firefoxprofile 
#    driver = webdriver.Firefox(options=options)
#    driver.get("https://web.whatsapp.com/")
#    wait = WebDriverWait(driver, 5200)
#    wait.until(EC.visibility_of_element_located((
#        By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/header/header/div/div[1]/h1")))
#    # waiting till the whatsapp is properly
#    # loaded all its content in the webbrowser
#    time.sleep(10)
#    for to,messagelist in content.items():
#        for message in messagelist:
#            logger.info("sending %s to %s",  message, to)
#            sendMessage(driver, to, message)
#
#    # sleeping isn't recommended; doing this 
#    # till i whatsapp send the message
#    time.sleep(20)
#    logger.info('[end]')
#    driver.quit()