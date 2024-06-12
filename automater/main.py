"""
simple script that automatically sends a message through
whatsapp to a person at a given time; 
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import sys

if __name__ == "__main__":

    # loading firefox driver
    driver = webdriver.Firefox()
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 120)

    # waiting till the user signin into
    # whatsapp web
    input("press enter to continue...")

    """
    everything from this point onwards is the
    clicking and typing;
    1. look for the search box xpath
    2. clear the text if present
    3. type the contact name
    4. wait until its searched
    5. press enter to grab the first result
    6. type the message
    7. send
    """

    # search_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div[1]/p")
    search_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div")
    # clear the search box
    search_box.clear()

    """
    need to find the correct xpath here; i am just too lazy to do 
    so; this is the reason i enter each character one by one
    """
    name = ""
    for i in name:
        search_box.send_keys(i)
    
    try:
        actions = ActionChains()
        actions.send_keys(Keys.Enter)
        actions.send_keys("test message")
        actions.send_keys(Keys.Enter)
        actions.perform()
    except NoSuchElementException:
        driver.quit()
        sys.exit()

    input("wait")

    driver.quit()
