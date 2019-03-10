# coding: utf-8
# from .karma import *
# for colored logs
from .aadhaar import XPAL_CONSOLE_FORMAT, XPAL_LEVEL_STYLES, XPAL_FIELD_STYLES
from uuid import uuid4
import configparser
import json
from pygments import highlight, lexers, formatters
from selenium import webdriver
import os
import coloredlogs
import logging
# For google sheets
DEBUG = False
# For twitter
# For youtube
# Selenium to automate browser work
# from selenium.webdriver.common.action_chains import ActionChains
# BeautifulSoup to make sense of what we got
# from BeautifulSoup import BeautifulSoup
# To make copies of files
# from shutil import copyfile
# Getting our basics
# Getting a logger which keeps track of things on console


def get_xpal_logger(name):
    xpallogger = logging.getLogger(name)
    coloredlogs.install(level="INFO", logger=xpallogger, fmt=XPAL_CONSOLE_FORMAT,
                        level_styles=XPAL_LEVEL_STYLES, field_styles=XPAL_FIELD_STYLES)
    return xpallogger


baselogger = get_xpal_logger("Xpal-Sutradhar")

# Getting a browser that lets us do browser based tasks


def get_browser(headless=False, path=None, logger=baselogger, **kwargs):
    logger.info("Launching a browser....")
    if headless is True:
        logger.info("...which has no head")
        os.environ['MOZ_HEADLESS'] = '1'

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
    if path is not None:
        firefox_profile.set_preference("browser.download.dir", path)
    firefox_profile.set_preference("browser.download.folderList", 2)
    firefox_profile.set_preference(
        "browser.download.manager.showWhenStarting", False)
    firefox_profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "text/plain, text/csv, image/jpeg, image/jpg",)
    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    return driver
