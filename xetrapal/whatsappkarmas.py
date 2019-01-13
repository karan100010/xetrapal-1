'''
यहां हम फेसबुक सम्बन्धी अस्त्रों का उल्लेख करेंगे
'''
# from .astra import *
import astra
import urllib2
import json
import karma
import os
# Fire and Forget Astras, to be run with {'msg':'run','func':function_object,'args':(),'kwargs':{}}

# Get value Astras, to be run with {'msg':'get','func':function_object,'args':(),'kwargs':{}}
# Use


def reply_random(browser, logger=astra.baselogger):
    text = os.popen("fortune -o").read().strip()
    send_text(text)


def send_text(browser, text, logger=astra.baselogger):
    logger.info("")
    textfield = browser.find_elements_by_class_name("_2S1VP")
    t = textfield[-1]
    t.click()
    t.send_keys(text)
    t = browser.find_element_by_class_name("_35EW6")
    t.click()
    karma.wait()
