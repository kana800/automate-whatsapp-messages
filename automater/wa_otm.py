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
logging.basicConfig(filename="db_wa_otm.log", encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# contact name is You by default
# will send a message to yourself
contact_name = "You"

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
    print(FFPROFILEPATH)
    firefoxprofile = webdriver.FirefoxProfile(FFPROFILEPATH)
    options.profile = firefoxprofile 
    service = webdriver.FirefoxService(executable_path='/usr/local/bin/geckodriver')
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://web.whatsapp.com/")
#    wait = WebDriverWait(driver, 5200)
#    wait.until(EC.visibility_of_element_located((
#        By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/header/header/div/div[1]/h1")))
#    message = re.split("\n", decode(message, 'unicode_escape'))
#    logger.debug("sending %s to %s", message, contact_name)
#    # everything from this point onwards is the
#    # clicking and typing;
#    # 1. create a new chat by typing CTRL+ALT+N 
#    # 2. type the contact name
#    # 3. press ENTER
#    # 6. type the message
#    # 7. press ENTER
#    # 8. press ESC
#    actions = ActionChains(driver)
#    # CTRL + ALT + N
#    actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('n').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
#    actions.send_keys(contact_name).perform()
#    body = driver.find_element(By.TAG_NAME, 'body')
#    # TODO: add error checking here
#    if (body.text.find("No results found")) == -1:
#        actions.send_keys(Keys.ENTER).perform()
#        for _message in message:
#            actions.send_keys(_message)
#            actions.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
#        actions.send_keys(Keys.ENTER).perform()
#        actions.send_keys(Keys.ESCAPE).perform()
#        # sleeping isn't recommended; doing this 
#        # till i whatsapp send the message
#        time.sleep(20)
#    else:
#        print("contact name cannot be found")
#        actions.send_keys(Keys.ESCAPE).perform()
#    logger.debug('[end]')
#    # sleeping isn't recommended; doing this 
#    # till i whatsapp send the message
#    time.sleep(20)
    input()
    driver.quit()
