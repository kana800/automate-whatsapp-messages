"""
small script to change the status 
of your whatsapp account
"""
import argparse
from sys import exit
from env import FFPROFILEPATH

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="change the whatsapp status")
    parser.add_argument("status",type=str, help="your whatsapp status")
    parser.add_argument("-headless", type=bool, default=True, help="run automator headless")
    args = parser.parse_args()

    message = args.status
    if len(message) >= 139:
        print("Message Is Too Long")
        exit(-1)

    # check the docs on how to bypass the whatsapp web login everytime
    # 1. create a new firefox profile; search -> about:profile
    # 2. go to whatsapp and login 
    # 3. enter the path
    options = FirefoxOptions()
    if args.headless: 
        options.add_argument("--headless")
    firefoxprofile = webdriver.FirefoxProfile(FFPROFILEPATH)
    options.profile = firefoxprofile 
    driver = webdriver.Firefox(options=options)
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 5200)
    wait.until(EC.visibility_of_element_located((
        By.XPATH,
        "/html/body/div[1]/div/div/div[2]/div[3]/header/header/div/div[1]/h1"
    )))
    
    # 1. load the profile and about
    # 2. /html/body/div[1]/div/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[4]/div[2]/div/span[2]/button/span
    actions = ActionChains(driver)
    # CTRL + ALT + P
    actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('p').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
    wait.until(EC.visibility_of_element_located((
        By.CSS_SELECTOR,
        "[title^='Click to edit About']"
    )))
    try:
        driver.find_element(By.CSS_SELECTOR,"[title^='Click to edit About']").click()
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        actions.send_keys(Keys.BACKSPACE).perform()
        actions.send_keys(message).perform()
        actions.send_keys(Keys.ENTER).perform()
        actions.send_keys(Keys.ESCAPE).perform()
    except Exception as e:
        print("Cannot Find The Edit Icon", file=sys.stderr)
    driver.quit()
