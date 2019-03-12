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
# from pygments import highlight, lexers, formatters
from uuid import uuid4
from .aadhaar import XPAL_WAIT_TIME
from . import astra
from . import smriti
import random
# import os


def load_xpal_smriti(configfilepath=None, **kwargs):
    profile = smriti.XetrapalSmriti.objects(configfile=configfilepath)
    if len(profile):
        return profile[0]
    else:
        profile = smriti.XetrapalSmriti(configfile=configfilepath)
        profile.save()
        return profile


def random_of_ranges(*ranges, **kwargs):
    return random.choice(random.choice(ranges))


def get_color_json(dictionary=None, logger=astra.baselogger, **kwargs):
    logger.info("Getting color json")
    formatted_json = get_formatted_json(dictionary)
    # colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter())
    return formatted_json


def get_formatted_json(dictionary=None, logger=astra.baselogger, **kwargs):
    formatted_json = json.dumps(dictionary, sort_keys=True, indent=4)
    return formatted_json


def load_config(configfile=None, logger=astra.baselogger, **kwargs):
    config = configparser.ConfigParser()
    config.read(configfile)
    return config


def get_section(config=None, sectionname=None, logger=astra.baselogger, **kwargs):
    if config.has_section(sectionname):
        p = config[sectionname]
        c = configparser.ConfigParser()
        a = {sectionname: dict(p)}
        c.read_dict(a)
        return c


def get_jeeva_config(name=None, path=None, sessionpathprefix=None, logger=astra.baselogger, **kwargs):
    if path is None:
        logger.error("Need a datapath")
        return None
    if sessionpathprefix is None:
        sessionpathprefix = "JeevaSession"
    configdict = {"Jeeva": {"datapath": path,
                            "sessionpathprefix": sessionpathprefix}}
    if name is not None:
        configdict['Jeeva']['name'] = name
    c = configparser.ConfigParser()
    c.read_dict(configdict)
    return c


def load_data_from_json(jsonpath=None, logger=astra.baselogger, **kwargs):
    data = {}
    if os.path.exists(jsonpath):
        try:

            with open(jsonpath) as f:
                data = json.load(f)
        except Exception as e:
            print("Failed to load file because" + str(e))
    return data


def save_data_to_jsonfile(data=None, filename=None, path=None, prefix=None, suffix=None, logger=astra.baselogger, **kwargs):
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


def download_file(url=None, path=None, filename=None, prefix=None, suffix=None, logger=astra.baselogger, **kwargs):
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


def export_table(rowdf=None, filename="table.csv", path=".", dataframe=False, logger=astra.baselogger, **kwargs):
    filepath = os.path.join(path, filename)
    try:
        rowdf.to_csv(filepath, encoding="utf-8")
        return filepath
    except Exception as e:
        logger.error("{} {}".format(type(e), str(e)))
        return "{} {}".format(type(e), str(e))


def scroll_page(browser=None, logger=astra.baselogger, **kwargs):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_up(browser=None, logger=astra.baselogger, **kwargs):
    browser.execute_script("window.scrollTo(0,window.scrollY-450);")


def scroll_to_bottom(browser=None, logger=astra.baselogger, **kwargs):
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


def close_modal(browser=None, logger=astra.baselogger, **kwargs):
    browser.find_element_by_link_text("Close").click()


def wait(waittime="medium", logger=astra.baselogger, **kwargs):
    t = XPAL_WAIT_TIME[waittime]
    interval = random_of_ranges(range(t-5, t+2), range(t-2, t+5))
    logger.info("Waiting for a %s duration : %s seconds" %
                (waittime, interval))
    time.sleep(interval)


def save_config(config=None, filename=None, logger=astra.baselogger, **kwargs):
    logger.warning("Saving config file in plain text in file "
                   + colored.stylize(filename, colored.fg("yellow")))
    with open(filename, "w") as configfile:
        config.write(configfile)


def get_aadesh(msg, func, args=[], kwargs={}, **kargs):
    aadesh = {'msg': msg, 'func': func, 'args': args, 'kwargs': kwargs}
    return aadesh
