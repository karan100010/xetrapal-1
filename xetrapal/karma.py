# coding: utf-8
'''

'''

# Configparser to load and read our configs
import configparser
# Time to keep time, OS to work with Linux, and Datetime to keep track of dates
import time
import os
from urllib.request import urlopen
import colored
# JSON to store everything
import json
# To get some colored outputs
from pygments import highlight, lexers, formatters

from uuid import uuid4
from .aadhaar import XPAL_WAIT_TIME, XPAL_UTC_OFFSET_TIMEDELTA
from . import astra
import random


def random_of_ranges(*ranges):
    return random.choice(random.choice(ranges))


def get_color_json(dictionary, logger=astra.baselogger):
    formatted_json = get_formatted_json(dictionary)
    colorful_json = highlight(unicode(
        formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter())
    return colorful_json


def get_formatted_json(dictionary, logger=astra.baselogger):
    formatted_json = json.dumps(dictionary, sort_keys=True, indent=4)
    return formatted_json


def load_config(configfile, logger=astra.baselogger):
    config = configparser.ConfigParser()
    config.read(configfile)
    return config


def get_section(config, sectionname, logger=astra.baselogger):
    if config.has_section(sectionname):
        p = config[sectionname]
        c = configparser.ConfigParser()
        a = {sectionname: dict(p)}
        c.read_dict(a)
        return c


def get_jeeva_config(name=None, datapath=None, sessionpathprefix=None, logger=astra.baselogger):
    if datapath is None:
        logger.error("Need a datapath")
        return None
    if sessionpathprefix is None:
        sessionpathprefix = "JeevaSession"
    configdict = {"Jeeva": {"datapath": datapath,
                            "sessionpathprefix": sessionpathprefix}}
    if name is not None:
        configdict['Jeeva']['name'] = name
    c = configparser.ConfigParser()
    c.read_dict(configdict)
    return c


def load_data_from_json(jsonpath, logger=astra.baselogger):
    data = {}
    if os.path.exists(jsonpath):
        try:

            with open(jsonpath) as f:
                data = json.load(f)
        except Exception as e:
            print("Failed to load file because" + str(e))
    return data


def save_data_to_jsonfile(data, filename=None, path=None, prefix=None, suffix=None, logger=astra.baselogger):
    if path is None:
        path = ""
    if filename is None:
        filename = str(uuid4())
    if prefix is not None:
        filename = prefix + filename
    if suffix is not None:
        filename = filename + suffix
    fname = os.path.join(path, filename)
    with open(fname, "w") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
    return fname


def download_file(url, path=None, filename=None, prefix=None, suffix=None, logger=astra.baselogger):
    if path is None:
        path = "."
    if filename is None:
        filename = str(uuid4())
    if prefix is not None:
        filename = prefix + filename
    if suffix is not None:
        filename = filename + suffix
    try:
        response = urlopen(url)
        data = response.read()
        fname = os.path.join(path, filename)
        f = open(fname, "w")
        f.write(data)
        f.close()

        return fname
    except Exception as e:
        logger.error("Error {}".format(str(e)))


def scroll_page(browser, logger=astra.baselogger):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_up(browser, logger=astra.baselogger):
    browser.execute_script("window.scrollTo(0,window.scrollY-450);")


def scroll_to_bottom(browser, logger=astra.baselogger):
    ticks_at_bottom = 0
    while True:
        js_scroll_code = "if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {return true;} else {return false;}"
        if browser.execute_script(js_scroll_code):
            if ticks_at_bottom > 1000:
                break
            else:
                ticks_at_bottom += 1
        else:
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            ticks_at_bottom = 0
    logger.info("At bottom of page")


def close_modal(browser, logger=astra.baselogger):
    browser.find_element_by_link_text("Close").click()


def wait(waittime="medium", logger=astra.baselogger):
    t = XPAL_WAIT_TIME[waittime]
    interval = random_of_ranges(range(t-5, t+2), range(t-2, t+5))
    logger.info("Waiting for a %s duration : %s seconds" %
                (waittime, interval))
    time.sleep(interval)


def save_config(config, filename, logger=astra.baselogger):
    logger.warning("Saving config file in plain text in file "
                   + colored.stylize(filename, colored.fg("yellow")))
    with open(filename, "w") as configfile:
        config.write(configfile)


def get_aadesh(msg, func, args=[], kwargs={}):
    aadesh = {'msg': msg, 'func': func, 'args': args, 'kwargs': kwargs}
    return aadesh


def get_utc_ts(ts):
    adjts = ts + XPAL_UTC_OFFSET_TIMEDELTA
    return adjts


def get_local_ts(ts):
    adjts = ts - XPAL_UTC_OFFSET_TIMEDELTA
    return adjts
