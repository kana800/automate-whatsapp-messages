"""
commandline application that send messages through
whatsapp 
"""
import time
import sys
import argparse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from multiprocessing.connection import Listener

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-activeserver", type=bool, default=False, help="run automater till you close the server")
    parser.add_argument("-headless", type=bool, default=False, help="run automator headless")
    args = parser.parse_args()

    # check the docs on how to bypass the whatsapp web login everytime
    # 1. create a new firefox profile; search -> about:profile
    # 2. go to whatsapp and login 
    # 3. enter the path
    options = FirefoxOptions()
    if args.headless: 
        options.add_argument("--headless")
    firefoxprofile = webdriver.FirefoxProfile("/home/kana/.mozilla/firefox/2f9sluw4.wa")
    options.profile = firefoxprofile 
    driver = webdriver.Firefox(options=options)
    driver.get("https://web.whatsapp.com/")
    WebDriverWait(driver, 5200)

    # contact name is You by default
    # will send a message to yourself
    contact_name = "You"

    # activating the socket connection 
    address = ('localhost', 6000)
    listener = Listener(address, authkey=b'secretkey')
    conn = listener.accept()

    # everything from this point onwards is the
    # clicking and typing;
    # 1. create a new chat by typing CTRL+ALT+N 
    # 2. type the contact name
    # 3. press ENTER
    # 6. type the message
    # 7. press ENTER
    # 8. press ESC
    actions = ActionChains(driver)
    while True:
        # format: send-message <contact-name> <message>
        msg = conn.recv()
        if msg == 'close':
            conn.close()
            break
        # TODO: add client feedback here; send message back
        # sending the message failed
        if (not msg.find("send") and 
            (not msg.find("name")) and (not msg.find("msg"))):
            raise Exception("send name:<name> msg:<message>")
            continue
        else:
            # CTRL + ALT + N
            actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('n').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
            actions.send_keys(contact_name)
            body = driver.find_element(By.TAG_NAME, 'body')
            # TODO: add error checking here
            if ( not body.text.find("No results found")):
                actions.send_keys(Keys.ENTER).perform()
                actions.send_keys(message)
                actions.send_keys(Keys.ENTER).perform()
                actions.send_keys(Keys.ESCAPE)
            else:
                raise Exception("contact name cannot be found")
                continue
    listener.close()
    driver.quit()
