"""
whatsapp server that runs in the background 
and listen to messages sent to the server
through sockets and execute them;
"""
import argparse
import logging
import re

from os import path
from os import name as osname

import sys
import json
import time

from env import FFPROFILEPATHW, FFPROFILEPATHL, LOGPATH

from codecs import decode

import socket
import threading
import queue

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)
logpath = path.join(LOGPATH, "db_wa_server.log")
logging.basicConfig(filename= logpath, encoding='utf-8', level=logging.INFO)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

msgqueue = queue.Queue()
IsRunning = True
WAactions = ['OTM', 'BLK','STA']

def sendMessage(driver:webdriver, to:str, message:list):
    actions = ActionChains(driver)
    # CTRL + ALT + N
    actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('n').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
    actions.send_keys(to).perform()
    body = driver.find_element(By.TAG_NAME, 'body')
    # TODO: add error checking here
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


def decodeMessage(driver, msg):
    """
    summary: decode the message 
    sent by the client
    FORMAT: <WAACTIONSTYPE> to:<TO> msg:<MESSAGE>
    WAACTIONTYPES
    - OTM
        FORMAT: OTM to:You msg:test message
    - OTP TODO: remove OTP
        FORMAT: OTP to:You msg:very long message here
    - BULK
        FORMAT: BLK to:You msg:<filepath>
    - STATUS
        FORMAT: STA msg:<filepath>
    return:
        decodestatus
    """
    actiontype = msg.lstrip()[:3]
    if actiontype.upper() not in WAactions:
        logger.info("Action Type Not Found")
        return -1 
    message = msg.lstrip()[3:]
    to_idx = message.find("to:")
    msg_idx = message.rfind("msg:")
    if to_idx == -1 or msg_idx == -1:
        logger.info("Wrong message format")
        return -1
    to = message[to_idx + 3:msg_idx].rstrip()
    content = message[msg_idx + 4:].lstrip()
    content_list = re.split("\n", decode(content, 'unicode_escape'))
    if actiontype == "OTM":
        sendMessage(driver, to, content_list)


if __name__ == "__main__":

    logger.info("[start]")
    # check the docs on how to bypass the whatsapp web login everytime
    # 1. create a new firefox profile; search -> about:profile
    # 2. go to whatsapp and login 
    # 3. enter the path
    options = FirefoxOptions()
    options.add_argument("--headless")
    FFPROFILEPATH = FFPROFILEPATHW if osname == "nt" else FFPROFILEPATHL

    firefoxprofile = webdriver.FirefoxProfile(FFPROFILEPATH)
    options.profile = firefoxprofile 
    driver = webdriver.Firefox(options=options)
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 100)
    time.sleep(200)
    # waiting till the whatsapp is properly
    # loaded all its content in the webbrowser
    address = ('localhost', 8000)
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(address)
        server.listen(0)
        print(f"listening on {address[0]}:{address[1]}")
        IsConnected = False
        while True:
            if IsConnected == False:
                client_socket, client_address = server.accept()
                print(f"connection accepted {client_address[0]}:{client_address[1]}")
                IsConnected = True

            if IsConnected:
                request = client_socket.recv(1024).decode("utf-8")
                print(f"({client_address[0]}:{client_address[1]}) -> {request}") 

                if request.lower() == "close":
                    client_socket.send("closed".encode("utf-8"))
                    IsConnected = False
                    client_socket.close()
                elif request.lower() == "quit":
                    client_socket.send("closed".encode("utf-8"))
                    IsConnected = False
                    client_socket.close()
                    break
                else:
                    decodeMessage(driver, request)
    except Exception as e:
        print(f"[MainLoop] Exception: {e}")
        logger.error(f"[MainLoop] Exception: {e}")
    finally:
        server.close()
    logger.info("[end]")
    driver.quit()
