#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
यहां हम whatsapp सम्बन्धी अस्त्रों का उल्लेख करेंगे
'''
# from .astra import *
from . import astra
from . import karma
from . import aadhaar
from bs4 import BeautifulSoup
import os
import datetime
from . import wasmriti
# Fire and Forget Astras, to be run with {'msg':'run','func':function_object,'args':(),'kwargs':{}}

# Get value Astras, to be run with {'msg':'get','func':function_object,'args':(),'kwargs':{}}
# Use
WAWCLASSMAP = {
    "sidepane": "//div[@id='pane-side']",
    "sidepane-item": "//div[@class='_2wP_Y']",
    "sidepane-back": "//span[@data-icon='back-light']",
    "sidepane-newchat": "//div[@title='New chat']",
    "sidepane-profile": "//div[contains(@class,'_2vPAk')]",
    "menu-launcher": "//div[@role='button' and @title='Menu']",
    "menu-button-newchat": "//div[@role='button' and @title='New chat']",
    "menu-button-profile": "//div[@role='button' and @title='Profile']",
    "sidepane-searchbox": "//input[@title='Search or start new chat']",
    "convpane": "//div[@class='_2nmDZ']",
    "convpane-item": "//div[@class='vW7d1']",

}


def wa_get_element(element=None, multi=False, wabrowser=None, logger=astra.baselogger, **kwargs):
    '''
    Gets a specified element from a whatsapp web signed in browser
    Arguments:
        element - the name of the element to be looked up in WAWCLASSMAP
        multi - specifies whether to get multiple elements corresponding to the xpath specified (True if multiple)
        wabrowser - handle to a whatsapp signed in browser session, use wa_test_login to test if logged in
        logger - which logger to write output to
    Returns:
        A selenium web element if successful, None if fails
    '''
    try:
        if multi is False:
            return wabrowser.find_element_by_xpath(WAWCLASSMAP[element])
        else:
            return wabrowser.find_elements_by_xpath(WAWCLASSMAP[element])
    except Exception as e:
        logger.error("{} {}".format(type(e), str(e)))
        return None


def wa_click_element(element=None, wabrowser=None, logger=astra.baselogger, **kwargs):
    '''
    Clicks a specified element from a whatsapp web signed in browser
    Arguments:
        element - the name of the element to be looked up in WAWCLASSMAP
        wabrowser - handle to a whatsapp signed in browser session, use wa_test_login to test if logged in
        logger - which logger to write output to
    Returns:
        True if successful, False if fails
    '''

    try:
        elem = wa_get_element(element=element, wabrowser=wabrowser, logger=logger, **kwargs)
        if elem is not None:
            elem.click()
            logger.info("Clicked element {}".format(element))
            return True
        else:
            logger.error("Could not find element {}".format(element))
            return False
    except Exception as e:
        logger.error("{} {}  in trying to click the element {}".format(type(e), str(e), element))
        return False


def wa_send_keys_to_element(element=None, keys=None, clearfirst=False, wabrowser=None, logger=astra.baselogger, **kwargs):
    '''
    Sends specified keys to a specified element from a whatsapp web signed in browser
    Arguments:
        element - the name of the element to be looked up in WAWCLASSMAP
        keys - keys to send, can be a string or a valid selenium.webdriver.common.keys Keys member
        wabrowser - handle to a whatsapp signed in browser session, use wa_test_login to test if logged in
        logger - which logger to write output to
    Returns:
        True if successful, False if fails
    '''
    try:
        elem = wa_get_element(element=element, wabrowser=wabrowser, logger=logger, **kwargs)
        if elem is not None:
            if clearfirst:
                elem.clear()
            elem.send_keys(keys)
            logger.info("Sent keys '{}' to element {}".format(keys, element))
            return True
        else:
            logger.error("Could not locate element {}".format(element))
            return False
    except Exception as e:
        logger.error("{} {} sending keys {} to element {}".format(type(e), str(e), keys, element))
        return False


def wa_test_login(wabrowser=None, logger=astra.baselogger, **kwargs):
    '''
    Tests if a web browser is signed into whatsapp
    Arguments:
        wabrowser - handle to a whatsapp signed in browser session, use wa_test_login to test if logged in
        logger - which logger to write output to
    Returns:
        True if logged in, False if not
    '''
    logger.info("Testing for Whatsapp Web Login by checking if the side pane is loaded...")
    try:
        sidepane = wa_get_element("sidepane", wabrowser=wabrowser, logeer=logger)
        if sidepane is not None:
            wabrowser.execute_script("arguments[0].scrollTo(0,0)", sidepane)
            logger.info("Whatsapp Web is logged in")
            return True
    except Exception as e:
        logger.error("Error:{} {}. Whatsapp Web doesn't seem to be logged in. Maybe try again later?".format(type(e), str(e)))
        return False


def wa_login(wabrowser=None, logger=astra.baselogger, tries=3, **kwargs):
    '''
    Opens a web browser and presents it for QR scan, then tests if its logged in
    Arguments:
        wabrowser - handle to a browser session, uses wa_test_login to test if logged in
        logger - which logger to write output to
    Returns:
        True if logged in, False if not
    '''
    logger.info("Attempting to access Whatsapp Web")
    wabrowser.get("https://web.whatsapp.com")
    logger.info("\n ***************************************\n Please scan the QR code in the browser with your phone's Whatsapp App\n ***************************************\n")
    for i in range(tries):
        karma.wait(logger=logger, waittime="long")
        if wa_test_login(wabrowser=wabrowser, logger=logger):
            break


def wa_get_conversations(all=False, scrolls=10, wabrowser=None, logger=astra.baselogger, **kwargs):
    '''
    Gets a list of conversations from the currently open whatsapp signed in browser as a list of dicts
    Arguments:
        wabrowser - handle to a whatsapp signed in browser session, use wa_test_login to test if logged in
        logger - which logger to write output to
    Returns:
        True if logged in, False if not
    '''
    conversations = []
    sidepane = wa_get_element("sidepane", wabrowser=wabrowser, logger=logger)
    wabrowser.execute_script("arguments[0].scrollTo(0,0)", sidepane)
    convnames = []
    m = 0
    newm = 1
    scrolled = 0
    while True:
        m = len(convnames)
        # recentList = wabrowser.find_elements_by_class_name("_2wP_Y")
        recentList = wa_get_element("sidepane-item", multi=True, wabrowser=wabrowser, logger=logger)
        for conv in recentList:
            try:
                convdict = {}
                convdict['display_name'] = conv.text.split("\n")[0]
                convdict['display_lines'] = conv.text.split("\n")
                if convdict['display_name'] not in [c['display_name'] for c in conversations] and convdict['display_name'] not in ["MESSAGES", "CHATS", "CONTACTS"]:
                    conversations.append(convdict)
            except Exception as e:
                logger.error(
                    "Could not parse conversation {} {}".format(type(e), str(e)))
                continue
        newm = len(conversations)
        if newm == m or all is False or scrolled == scrolls:
            break
        scrolled += 1
        wabrowser.execute_script("arguments[0].scrollBy(0,500)", sidepane)
        karma.wait(logger=logger, waittime="medium")
    return conversations


def wa_search_conversations(text=None, exact=True, all=False, scrolls=10, wabrowser=None, logger=astra.baselogger, **kwargs):
    wa_send_keys_to_element("sidepane-searchbox", text, clearfirst=True, wabrowser=wabrowser, logger=logger)
    karma.wait(logger=logger, waittime="medium")
    convs = wa_get_conversations(all=all, scrolls=scrolls, wabrowser=wabrowser, logger=logger)
    if exact is True:
        for conv in convs:
            if conv['display_name'] == text:
                return conv
    else:
        return convs


def wa_get_conv_messages(wabrowser=None, conversation=None, historical=False, logger=astra.baselogger, scrolls=10, **kwargs):
    logger.info("Searching for messages in conversation {}".format(conversation.display_name))
    # p = wa_get_conv_message_lines(wabrowser=wabrowser, text=conversation.display_name, historical=historical, logger=logger, scrolls=scrolls)
    messages = []
    # seen_messages = []
    # return messages
    '''
    for message in p:
        m = wa_get_message(message, wabrowser, logger=logger)
        if type(m) == dict and m != {}:
            messages.append(m)
    '''
    return messages


def wa_select_conv(conversation=None, text=None, wabrowser=None, logger=astra.baselogger, **kwargs):
    pane = wa_get_element("sidepane", wabrowser=wabrowser, logger=logger)
    wabrowser.execute_script("arguments[0].scrollTo(0,0)", pane)
    convnames = []
    while True:
        m = len(convnames)
        recentList = wa_get_element("sidepane-item", multi=True, wabrowser=wabrowser, logger=logger)
        for conv in recentList:
            try:
                convdict = {}
                convdict['display_name'] = conv.text.split("\n")[0]
                convdict['display_lines'] = conv.text.split("\n")
                if text is not None and text in conv.text:
                    conv.click()
                    return True
                elif conversation is not None and conversation.display_name == convdict['display_name']:
                    conv.click()
                    return True
                else:
                    convnames.append(convdict['display_name'])
            except Exception as e:
                logger.error(
                    "Could not parse conversation {} {}".format(type(e), str(e)))
                continue
        newm = len(convnames)
        if newm == m:
            logger.error("No matching conversation found for {}".format(text))
            return False
        wabrowser.execute_script("arguments[0].scrollBy(0,500)", pane)


def wa_get_message(line=None, wabrowser=None, logger=astra.baselogger, **kwargs):
    msgdict = {}
    try:
        wabrowser.execute_script("arguments[0].scrollIntoView(true)", line)
        linebs = BeautifulSoup(line.get_property("innerHTML"), features="html.parser")
        messages_in = linebs.find_all("div", {"class": "message-in"})
        messages_out = linebs.find_all("div", {"class": "message-out"})
        message = messages_in+messages_out
        # TODO: Replace with Whatsapp Classmap in Xetrapal
        if len(message):
            msg = linebs.find("div", {"class": "copyable-text"})
            logger.info(msg)
            if msg:
                msgts = msg.get("data-pre-plain-text").split("] ")[0].replace("[", "").replace("]", "")
                msgsender = msg.get("data-pre-plain-text").split("] ")[1]
                if "m" in msgts.lower():
                    msgdict["created_timestamp"] = aadhaar.get_utc_ts(datetime.datetime.strptime(msgts, "%H:%M %p, %m/%d/%Y"))
                else:
                    msgdict["created_timestamp"] = aadhaar.get_utc_ts(datetime.datetime.strptime(msgts, "%H:%M, %m/%d/%Y"))
                msgdict['sender'] = {"platform": "whatsapp"}
                if not aadhaar.engalpha.search(msgsender):
                    msgdict['sender']['mobile_num'] = msgsender.replace(": ", "").replace(" ", "")
                    logger.info("Mobile Num: {}".format(msgdict['sender']))
                else:
                    msgdict['sender']['whatsapp_contact'] = msgsender.replace(": ", "")
                    logger.info("Whatsapp Contact: {}".format(msgdict['sender']))
                msgdict['text_lines'] = [x.replace("'", "") for x in msg.strings]
                try:
                    msgdict['sender']['displayed_sender'] = linebs.find("span", {"class": "RZ7GO"}).text
                    msgdict['sender']['displayed_sender_name'] = linebs.find("span", {"class": "_3Ye_R"}).text
                except Exception as e:
                    logger.error("Could not get display name and sender")
                images = message[0].find_all("img")
                if len(images):
                    image = line.find_element_by_tag_name("img")
                    if "blob" in image.get_attribute("src"):
                        image.click()
                        karma.wait(logger=logger)
                        files = os.listdir(wabrowser.profile.default_preferences['browser.download.dir'])
                        wabrowser.find_element_by_xpath("//div[@title='Download']").click()
                        karma.wait(waittime="long", logger=logger)
                        newfiles = os.listdir(wabrowser.profile.default_preferences['browser.download.dir'])
                        logger.info("Downloaded file {}".format(list(set(newfiles)-set(files))[0]))
                        msgdict['file'] = os.path.join(wabrowser.profile.default_preferences['browser.download.dir'], list(set(newfiles)-set(files))[0])
                        karma.wait(logger=logger)
                        wabrowser.find_element_by_xpath("//div[@title='Close']").click()
                        karma.wait(logger=logger)
            if msgdict != {}:
                msgdict['platform'] = "whatsapp"
                logger.info(msgdict)
                return msgdict
        else:
            return "No message in line"
    except Exception as e:
        logger.error("{} {}".format(type(e), str(e)))
        return "{} {}".format(type(e), str(e))


def wa_get_cur_conv_messages(historical=False, scrolls=2, wabrowser=None, logger=astra.baselogger, **kwargs):
    convpane = wa_get_element("convpane", wabrowser=wabrowser, logger=logger)
    scrolled = 0
    lines = []
    while True:
        numlines = len(lines)
        wabrowser.execute_script("arguments[0].scrollTo(0,0)", convpane)
        # lines = wabrowser.find_elements_by_class_name("vW7d1")
        lines = wa_get_element("convpane-item", multi=True, wabrowser=wabrowser, logger=logger)
        karma.wait(waittime="long", logger=logger)
        newnumlines = len(lines)
        if historical is not True:
            if scrolled == scrolls:
                break
        if newnumlines == numlines:
            break
        scrolled += 1
    msgs = []
    for line in lines:
        msgdict = wa_get_message(line=line, wabrowser=wabrowser, logger=logger)
        logger.info("{}".format(msgdict))
        if type(msgdict) == dict:
            msg = wasmriti.WhatsappMessage.objects(**msgdict)
            if len(msg):
                logger.error("Duplicate")
            else:
                msg = wasmriti.WhatsappMessage(**msgdict)
                msg.save()
                msgs.append(msg)
    return msgs
    # return lines


def wa_add_conversation(convdict=None, logger=astra.baselogger, **kwargs):
    try:
        waconversation = wasmriti.WhatsappConversation.objects(display_name=convdict['display_name'])
        if len(waconversation) == 0:
            waconversation = wasmriti.WhatsappConversation(**convdict)
            waconversation.save()
            return [waconversation]
        else:
            logger.error("Conversation already being tracked")
            waconversation = waconversation[0]
            waconversation.update(**convdict)
            waconversation.save()
            waconversation.reload()
            return [waconversation]
    except Exception as e:
        logger.error("{} {} trying to add conversation dict {}".format(type(e), str(e), convdict))
        return "{} {} trying to add conversation dict {}".format(type(e), str(e), convdict)


def wa_update_conversation(conversation=None, wabrowser=None, logger=astra.baselogger, **kwargs):
    logger.info("Trying to update conversation {}".format(conversation.display_name))
    try:
        if wa_select_conv(conversation=conversation, wabrowser=wabrowser, logger=logger):
            convs = wa_get_conversations(wabrowser=wabrowser, logger=logger)
            for conv in convs:
                if conv['display_name'] == conversation.display_name:
                    conversation.update(**conv)
                    conversation.save()
                    conversation.reload()
                    logger.info("Successfully updated conversation {}".format(conversation.display_name))
                    return True
        else:
            logger.error("Could not select conversation {}".format(conversation.display_name))
            return False
    except Exception as e:
        logger.error("{} {} trying to update conversation {}".format(type(e), str(e), conversation.display_name))
        return "{} {} trying to update conversation {}".format(type(e), str(e), conversation.display_name)


def wa_send_text(wabrowser, text, logger=astra.baselogger):
    logger.info("Sending message {}".format(text))
    textfield = wabrowser.find_elements_by_class_name("_2S1VP")
    t = textfield[-1]
    t.click()
    t.send_keys(text)
    t = wabrowser.find_element_by_class_name("_35EW6")
    t.click()
    karma.wait(logger=logger)


def wa_reply_random(wabrowser, logger=astra.baselogger):
    text = os.popen("fortune").read().strip()
    logger.info(
        "Sending random reply to current conversation in browser {}".format(text))
    wa_send_text(wabrowser, text)


def wa_send_message_to_conv(wabrowser, convtext, text, logger=astra.baselogger):
    logger.info("Trying to locate conversation with text {}".format(convtext))
    resp = wa_select_conv(wabrowser, convtext)
    if "error" not in resp:
        logger.info("Sending text {} to selected conv {}".format(text, resp))
        wa_send_text(wabrowser, text)


def wa_get_images_for_users(wabrowser, conversations, logger=astra.baselogger):
    # people = browser.find_elements_by_class_name("_2wP_Y")
    names = []
    image_list = []
    for conv in range(len(conversations)):
        name_div = conversations[conv].find_elements_by_class_name("_3TEwt")
        if len(name_div) != 0:
            name = name_div[0].find_element_by_tag_name("span")
            # name_=name.find_element_by_tag_name("span")
            name_ = name.get_attribute("title")
        else:
            name_ = "not found " + str(conv)
        logger.info("adding " + name_ + " to list names")
        names.append(name_)
    for i in range(len(conversations)):
        image_div = conversations[i].find_elements_by_class_name("_1WliW")
        if len(image_div) != 0:
            image_tag = image_div[0].find_elements_by_tag_name("img")
        else:

            image_tag = []
            i + 1
        if len(image_tag) != 0:
            link = image_tag[0].get_attribute("src")
            if "https" not in link:
                link = "not found"
        else:
            link = "not found"

        logger.info("adding " + link + " to image list")
        image_list.append(link)
    dic = dict(zip(names, image_list))
    return dic
# a=get_images_for_users(browser)\


def wa_get_images_from_contacts(wabrowser=None):
    contact_chat = wabrowser.find_elements_by_class_name("rAUz7")
    for i in range(len(contact_chat)):
        icon = contact_chat[i].find_element_by_tag_name("span")
        chat = icon.get_attribute("data-icon")
        if chat == u'chat':
            contact_chat[i].click()
            print("yes")
            break
        else:
            print("not this")
    return wa_get_images_for_users(wabrowser)
