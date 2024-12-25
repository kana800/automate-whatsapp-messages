"""
send one-time message through whatsapp
usage:
    wa_otm.py <recepient> <medium> <content>
example:
    wa_otm.py "You" "file" "content.txt"
    wa_otm.py "You" "message" "hi!!"
"""
import argparse
import re
import logging

from os.path import exists
from os import name as osname
from codecs import decode
from sys import exit
import time

from env import FFPROFILEPATHW, FFPROFILEPATHL

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)
logging.basicConfig(filename="db_wa_otm.log", encoding='utf-8', level=logging.ERROR)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# contact name is You by default
# will send a message to yourself
contact_name = "You"

def sendMessage(driver:webdriver, to:str, message:list):
    actions = ActionChains(driver)
    # CTRL + ALT + N
    actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('n').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
    actions.send_keys(to).perform()
    body = driver.find_element(By.TAG_NAME, 'body')
    # TODO: add error checking here
    #logger.info(f"sending message to:{to}")
    if (body.text.find("No results found")) == -1:
        actions.send_keys(Keys.ENTER).perform()
        for _message in message:
            actions.send_keys(_message)
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

    logger.debug('[start]')

    parser = argparse.ArgumentParser(description="send a whatsapp message")
    parser.add_argument("recepient", type=str, help="recepient of the message")
    parser.add_argument("medium", type=str, choices=["message","file"], help="what type of content; either direct message or a file")
    parser.add_argument("content", type=str, help="if message; type message or else enter filepath")

    args = parser.parse_args()
    
    contact_name = args.recepient.lstrip().rstrip()

    if args.medium == "file" and exists(args.content):
        with open(args.content,'r') as file:
            message = file.read()
    elif args.medium == "message":
        message = args.content.lstrip().rstrip()
    else:
        logger.debug("%s doesn't exist; exiting program", args.content)
        exit(-1)

    # check the docs on how to bypass the whatsapp web login everytime
    # 1. create a new firefox profile; search -> about:profile
    # 2. go to whatsapp and login 
    # 3. enter the path
    options = FirefoxOptions()
    options.add_argument("--headless")
    FFPROFILEPATH = FFPROFILEPATHW if osname == "nt" else FFPROFILEPATHL
    firefoxprofile = webdriver.FirefoxProfile(FFPROFILEPATH)
    options.profile = firefoxprofile 
    if osname == 'posix':
        service = webdriver.FirefoxService(executable_path='/usr/local/bin/geckodriver')
        driver = webdriver.Firefox(service=service, options=options)
    else:
        driver = webdriver.Firefox(options=options)
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 180)
    try:
        wait.until(
                EC.invisibility_of_element_located((By.ID, "wa_web_initial_startup"))
        )
        wait.until(
            EC.presence_of_element_located((By.ID, "app"))
        )
        # waiting until 1 minute to load up everything 
        # before doing any checks
        time.sleep(60)
        # checking if we need to login to the system
        loginpage = re.search(r"Log into WhatsApp Web", driver.page_source)
        if not loginpage:
            message = re.split("\n", decode(message, 'unicode_escape'))
            sendMessage(driver, contact_name, message)
    except Exception as e:
        print("Login In Error: please Log In and run the program")
        logger.error("Error: Login Page (%s)", e)
    driver.quit()