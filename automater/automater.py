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


# contact name is You by default
# will send a message to yourself
contact_name = "You"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-headless", type=bool, default=False, help="run automator headless")
    parser.add_argument("contactname",type=str, default="You", help="contact name (example:'sam smith')")
    parser.add_argument("message",type=str, default="this is a test message", help="message ( example:'this is a test message'")
    args = parser.parse_args()

    # check the docs on how to bypass the whatsapp web login everytime
    # 1. create a new firefox profile; search -> about:profile
    # 2. go to whatsapp and login 
    # 3. enter the path
    options = FirefoxOptions()
    if args.headless: 
        options.add_argument("--headless")
    firefoxprofile = webdriver.FirefoxProfile()
    options.profile = firefoxprofile 
    driver = webdriver.Firefox(options=options)
    driver.get("https://web.whatsapp.com/")
    WebDriverWait(driver, 5200)

    # everything from this point onwards is the
    # clicking and typing;
    # 1. create a new chat by typing CTRL+ALT+N 
    # 2. type the contact name
    # 3. press ENTER
    # 6. type the message
    # 7. press ENTER
    # 8. press ESC
    actions = ActionChains(driver)
    # format: send-message <contact-name> <message>
    # TODO: add client feedback here; send message back
    # sending the message failed
    contact_name = args.contactname
    message = args.message
    print(f"contact name: {contact_name} | message: {message}")
    if message and contact_name:
        # CTRL + ALT + N
        actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('n').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
        actions.send_keys(contact_name).perform()
        body = driver.find_element(By.TAG_NAME, 'body')
        # TODO: add error checking here
        if (body.text.find("No results found")) == -1:
            actions.send_keys(Keys.ENTER).perform()
            actions.send_keys(message)
            actions.send_keys(Keys.ENTER).perform()
            actions.send_keys(Keys.ESCAPE).perform()
        else:
            print("contact name cannot be found")
            actions.send_keys(Keys.ESCAPE).perform()
    else:
        print("request cannot be processed")
    driver.quit()
