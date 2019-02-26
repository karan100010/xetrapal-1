#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
यहां हम whatsapp सम्बन्धी अस्त्रों का उल्लेख करेंगे
'''
# from .astra import *
from . import astra
from . import karma
import os
# Fire and Forget Astras, to be run with {'msg':'run','func':function_object,'args':(),'kwargs':{}}

# Get value Astras, to be run with {'msg':'get','func':function_object,'args':(),'kwargs':{}}
# Use


def get_conversations(browser, logger=astra.baselogger):
    conversations = browser.find_elements_by_class_name("_2wP_Y")
    convdicts = []
    for conv in conversations:
        convdict = {}
        convdict['display_name'] = conv.text.split("\n")[0]
        convdict['display_lines'] = conv.text.split("\n")
        if convdict['display_name'] not in [c['display_name'] for c in convdicts] and convdict['display_name'] not in ["MESSAGES", "CHATS", "CONTACTS"]:
            convdicts.append(convdict)
    return convdicts


def search_conversations(wabrowser, text, logger=astra.baselogger):
    convsearchbox = wabrowser.find_element_by_xpath("//input[@title='Search or start new chat']")
    convsearchbox.send_keys(text)
    karma.wait()
    cdicts = get_conversations(wabrowser)
    return cdicts


def reply_random(browser, logger=astra.baselogger):
    text = os.popen("fortune").read().strip()
    logger.info(
        "Sending random reply to current conversation in browser {}".format(text))
    send_text(browser, text)


def send_text(browser, text, logger=astra.baselogger):
    logger.info("Sending message {}".format(text))
    textfield = browser.find_elements_by_class_name("_2S1VP")
    t = textfield[-1]
    t.click()
    t.send_keys(text)
    t = browser.find_element_by_class_name("_35EW6")
    t.click()
    karma.wait()


def build_convdictlist(wabrowser, logger=astra.baselogger):
    pane = wabrowser.find_element_by_id("pane-side")
    wabrowser.execute_script("arguments[0].scrollTo(0,0)", pane)
    convnames = []
    convdicts = []
    while True:
        lendicts = len(convdicts)
        lennames = len(convnames)
        recentList = wabrowser.find_elements_by_class_name("_2wP_Y")
        for conv in recentList:
            try:
                convdict = {}
                convdict['display_name'] = conv.text.split("\n")[0]
                convdict['display_lines'] = conv.text.split("\n")
                if convdict['display_name'] not in convnames:
                    convdicts.append(convdict)
                    convnames.append(convdict['display_name'])
            except Exception as e:
                logger.error(
                    "Could not parse conversation {} {}".format(type(e), str(e)))
                continue
        newlendicts = len(convdicts)
        newlennames = len(convnames)
        logger.info("Last run {} {}, this run {} {} conversations tracked".format(
            lendicts, lennames, newlendicts, newlennames))
        if newlennames == lennames:
            break
        wabrowser.execute_script("arguments[0].scrollBy(0,500)", pane)
    return convdicts


def select_conv(wabrowser, text, logger=astra.baselogger):
    pane = wabrowser.find_element_by_id("pane-side")
    wabrowser.execute_script("arguments[0].scrollTo(0,0)", pane)
    convnames = []
    while True:
        m = len(convnames)
        recentList = wabrowser.find_elements_by_class_name("_2wP_Y")
        for conv in recentList:
            try:
                convdict = {}
                convdict['display_name'] = conv.text.split("\n")[0]
                convdict['display_lines'] = conv.text.split("\n")
                if text in conv.text:
                    conv.click()
                    return convdict['display_name']
                else:
                    convnames.append(convdict['display_name'])
            except Exception as e:
                logger.error(
                    "Could not parse conversation {} {}".format(type(e), str(e)))
                continue
        newm = len(convnames)
        if newm == m:
            logger.error("No matching conversation found for {}".format(text))
            return "error: No matching conversation found for {}".format(text)
            break
        wabrowser.execute_script("arguments[0].scrollBy(0,500)", pane)


def send_message_to_conv(wabrowser, convtext, text, logger=astra.baselogger):
    logger.info("Trying to locate conversation with text {}".format(convtext))
    resp = select_conv(wabrowser, convtext)
    if "error" not in resp:
        logger.info("Sending text {} to selected conv {}".format(text, resp))
        send_text(wabrowser, text)
