"""
send one-time message through whatsapp
"""
import argparse
from os.path import dirname
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# contact name is You by default
# will send a message to yourself
contact_name = "You"

JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""

def drag_and_drop_file(drop_target, path):
    driver = drop_target.parent
    file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
    file_input._execute('sendKeysToElement', {'value': [path], 'text': path})

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-headless", type=bool, default=False, help="run automator headless")
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
    wait = WebDriverWait(driver, 5200)
    wait.until(EC.visibility_of_element_located((
        By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/header/header/div/div[1]/h1")))
    message = re.split("/n","test message/nwith another test message")
    # everything from this point onwards is the
    # clicking and typing;
    # 1. create a new chat by typing CTRL+ALT+N 
    # 2. type the contact name
    # 3. press ENTER
    # 6. type the message
    # 7. press ENTER
    # 8. press ESC
    # generate a alert via javascript 
    actions = ActionChains(driver)
    # CTRL + ALT + N
    actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('n').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
    actions.send_keys(contact_name).perform()
    body = driver.find_element(By.TAG_NAME, 'body')
    # TODO: add error checking here
    if (body.text.find("No results found")) == -1:
        actions.send_keys(Keys.ENTER).perform()
        for _message in message:
            actions.send_keys(_message)
            actions.key_down(Keys.SHIFT).key_down(Keys.ENTER).perform()
        actions.key_up(Keys.SHIFT).perform()
        actions.send_keys(Keys.ENTER).perform()
        actions.send_keys(Keys.ESCAPE).perform()
    else:
        print("contact name cannot be found")
        actions.send_keys(Keys.ESCAPE).perform()
    driver.quit()
