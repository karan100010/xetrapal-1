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
from copy import deepcopy
from . import wasmriti
import pandas
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
    "convpane-item": "//div[contains(@class, 'vW7d1')]",
    "convpane-item-sender": ".//div[contains(@class, '_111ze')]",
    "media-download-button": "//div[@title='Download']",
    "media-close-button": "//div[@title='Close']",
    "message-out": ".//div[contains(@class,'message-out')]",
    "message-in": ".//div[contains(@class,'message-in')]",
    "copyable-text": ".//div[contains(@class,'copyable-text')]",
    "selectable-text": ".//span[contains(@class,'selectable-text')]",
    "fallbacktimestamp": ".//span[@class='_3EFt_']",
    "reply-to": ".//div[@class='_3CVlE']",
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


def wa_get_self_profile(path=None, pic=False, wabrowser=None, logger=astra.baselogger, **kwargs):
    logger.info("Trying to get self profile")
    try:
        wa_click_element("menu-launcher", wabrowser=wabrowser, logger=logger)
        karma.wait(logger=logger, waittime="short")
        wa_click_element("menu-button-profile", wabrowser=wabrowser, logger=logger)
        karma.wait(logger=logger)
        profilepane = wa_get_element("sidepane-profile", wabrowser=wabrowser, logger=logger)
        whatsapp_contact = profilepane.text.split("\n")[2]
        profiledict = {"platform": "whatsapp", "whatsapp_contact": whatsapp_contact}
        profile = wa_add_profile_smriti(profiledict, logger=logger)[0]
        if not hasattr(profile, "files"):
            profile.files = []
        if pic is True:
            profilepic = profilepane.find_element_by_tag_name("img")
            profilepic_path = os.path.join(path, "whatsapp_profile_"+str(profile.id)+"_"+str(datetime.datetime.utcnow().timestamp())+".png")
            profilepic.screenshot(profilepic_path)
            profile.files.append(profilepic_path)
            profile.save()
            profile.reload()
        wa_click_element("sidepane-back", wabrowser=wabrowser, logger=logger)
        return profile
    except Exception as e:
        logger.error("{} {} trying to get own profile".format(type(e), str(e)))
        return None


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


def wa_add_conversation_smriti(convdict=None, logger=astra.baselogger, **kwargs):
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


def wa_update_conversation_smriti(conversation=None, wabrowser=None, logger=astra.baselogger, **kwargs):
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


def wa_select_conv(conversation=None, text=None, wabrowser=None, logger=astra.baselogger, **kwargs):
    if conversation is not None:
        text = conversation.display_name
    logger.info("Trying to select conversation {}".format(text))
    wa_get_element("sidepane-searchbox", wabrowser=wabrowser, logger=logger).clear()
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
                # elif conversation is not None and conversation.display_name == convdict['display_name']:
                #     conv.click()
                #     return True
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


def wa_get_conv_messages(conversation=None, historical=False,  scrolls=2, wabrowser=None, logger=astra.baselogger, **kwargs):
    logger.info("Trying to get messages for conversation {}".format(conversation.display_name))
    wa_select_conv(conversation=conversation, wabrowser=wabrowser, logger=logger)
    messages = wa_get_cur_conv_messages(historical=historical, scrolls=scrolls, wabrowser=wabrowser, logger=logger)
    # p = wa_get_conv_message_lines(wabrowser=wabrowser, text=conversation.display_name, historical=historical, logger=logger, scrolls=scrolls)

    for msg in messages:
        if type(msg) == str:
            messages.pop(msg)
        else:
            msg.observed_in = conversation
            msg.save()
            msg.reload()
    return messages


def wa_get_profile_smriti(profiledictin=None, logger=astra.baselogger, **kwargs):
    profiledict = deepcopy(profiledictin)
    if "senderlines" in profiledict.keys():
        profiledict.pop("senderlines")
    for key in profiledict.keys():
        if type(profiledict[key]) == str and not aadhaar.engalpha.search(profiledict[key]):
            profiledict[key] = profiledict[key].replace(" ", "")
        if key == "files":
            profiledict.pop("files")
    logger.info("Trying to get profile dict {}".format(profiledict))
    try:
        waprofile = wasmriti.WhatsappProfile.objects(**profiledict)
        return list(waprofile)
    except Exception as e:
        logger.error("{} {} trying to get profile dict {}".format(type(e), str(e), profiledict))
        return "{} {} trying to get profile dict {}".format(type(e), str(e), profiledict)


def wa_add_profile_smriti(profiledictin=None, logger=astra.baselogger, **kwargs):
    profiledict = deepcopy(profiledictin)
    if "senderlines" in profiledict.keys():
        profiledict.pop("senderlines")
    for key in profiledict.keys():
        if type(profiledict[key]) == str and not aadhaar.engalpha.search(profiledict[key]):
            profiledict[key] = profiledict[key].replace(" ", "")
    logger.info("Trying to add and get profile dict {}".format(profiledict))
    try:
        waprofile = wa_get_profile_smriti(profiledictin=profiledict, logger=logger)
        if len(waprofile):
            logger.error("Profile smriti already exists")
            return list(waprofile)
        else:
            profiledict['naam'] = []
            for key in ["whatsapp_contact", "displayed_sender_name", "displayed_sender", "mobile_num"]:
                if key in profiledict.keys():
                    profiledict['naam'].append(profiledict[key])
            profiledict['naam'] = list(set(profiledict['naam']))
            waprofile = wasmriti.WhatsappProfile(**profiledict)
            waprofile.save()
            waprofile.reload()
            return[waprofile]
    except Exception as e:
        logger.error("{} {} trying to get profile dict {}".format(type(e), str(e), profiledict))
        return "{} {} trying to get profile dict {}".format(type(e), str(e), profiledict)


# Needs cleanup


def wa_get_msg_dict(line=None, wabrowser=None, logger=astra.baselogger, **kwargs):
    wabrowser.execute_script("arguments[0].scrollIntoView(true)", line)
    msgdict = {"platform": "whatsapp", "sender": {"platform": "whatsapp"}, 'files': [], 'text_lines': []}
    messagein = line.find_elements_by_xpath(WAWCLASSMAP['message-in'])
    messageout = line.find_elements_by_xpath(WAWCLASSMAP['message-out'])
    messages = messagein+messageout
    if len(messageout) > 0:
        msgdict['sender']['self'] = True
    for message in messages:
        sender = message.find_elements_by_xpath(WAWCLASSMAP['convpane-item-sender'])
        msgdict['sender']['senderlines'] = [c.text.split("\n") for c in sender]
        if len(msgdict['sender']['senderlines']):
            msgsender = msgdict['sender']['senderlines'][0]
            msgdict['sender']['displayed_sender'] = msgsender[0]
            if len(msgsender) > 1:
                msgdict['sender']['displayed_sender_name'] = msgsender[1]
        selectable_text = message.find_elements_by_xpath(WAWCLASSMAP['selectable-text'])
        msgdict['selectable_text'] = [c.text for c in selectable_text]
        copyable_text = message.find_elements_by_xpath(WAWCLASSMAP['copyable-text'])
        msgdict['copyable_text'] = []
        for c in copyable_text:
            msgdict['copyable_text'].append(c.text)
            if c.get_attribute("data-pre-plain-text") is not None:
                ts = c.get_attribute("data-pre-plain-text").split("] ")[0].replace("[", "").replace("]", "")
                if "m" in ts.lower():
                    msgdict["created_timestamp"] = aadhaar.get_utc_ts(datetime.datetime.strptime(ts, "%H:%M %p, %m/%d/%Y"))
                else:
                    msgdict["created_timestamp"] = aadhaar.get_utc_ts(datetime.datetime.strptime(ts, "%H:%M, %m/%d/%Y"))
                msgsender = c.get_attribute("data-pre-plain-text").split("] ")[1]
                if not aadhaar.engalpha.search(msgsender):
                    msgdict['sender']['mobile_num'] = msgsender.replace(": ", "").replace(" ", "")
                # logger.info("Mobile Num: {}".format(msgdict['sender']))
            else:
                msgdict['sender']['whatsapp_contact'] = msgsender.replace(": ", "")
                # logger.info("Whatsapp Contact: {}".format(msgdict['sender']))
        images = message.find_elements_by_tag_name("img")
        msgdict['images'] = ["image: " + c.get_attribute("src") for c in images]
        links = message.find_elements_by_tag_name("a")
        msgdict['links'] = ["link: "+c.text for c in links]
        replyto = message.find_elements_by_xpath(WAWCLASSMAP['reply-to'])
        msgdict['reply_to'] = ["reply-to: "+c.text for x in replyto]

        if "created_timestamp" not in msgdict.keys():
            try:
                msgdict['created_timestamp'] = datetime.datetime.utcnow()
                ts = message.find_element_by_xpath(WAWCLASSMAP['fallbacktimestamp']).text
                if "m" in ts.lower():
                    tstime = aadhaar.get_utc_ts(datetime.datetime.strptime(ts, "%H:%M %p").replace(second=0, microsecond=0))
                else:
                    tstime = aadhaar.get_utc_ts(datetime.datetime.strptime(ts, "%H:%M").replace(second=0, microsecond=0))
                msgdict['created_timestamp'] = msgdict['created_timestamp'].replace(hour=tstime.hour, minute=tstime.minute, second=0, microsecond=0)
            except Exception as e:
                print(e)
        msgdict['text_lines'] = list(set(msgdict['copyable_text']+msgdict['selectable_text']+msgdict['links']+msgdict['images']+msgdict['reply_to']))
        return msgdict


def wa_get_message(line=None, wabrowser=None, logger=astra.baselogger, **kwargs):
    try:
        msgdict = wa_get_msg_dict(line=line, wabrowser=wabrowser, logger=logger)
        logger.info("{}".format(msgdict))
        msg = wa_get_message_smriti(msgdict, logger=logger)
        if type(msg) == list and msg != []:
            logger.error("Message smriti already exists")
            return msg[0]
        if len(msgdict['images']):
            image = line.find_element_by_tag_name("img")
            if "blob" in image.get_attribute("src"):
                logger.info("Trying to download image...")
                image.click()
                karma.wait(logger=logger)
                files = os.listdir(wabrowser.profile.default_preferences['browser.download.dir'])
                wa_click_element(element="media-download-button", wabrowser=wabrowser, logger=logger)
                # wabrowser.find_element_by_xpath("//div[@title='Download']").click()
                karma.wait(waittime="long", logger=logger)
                newfiles = os.listdir(wabrowser.profile.default_preferences['browser.download.dir'])
                logger.info("Downloaded file {}".format(list(set(newfiles)-set(files))[0]))
                # msgdict['file'] = os.path.join(wabrowser.profile.default_preferences['browser.download.dir'], list(set(newfiles)-set(files))[0])
                msgdict['files'].append(os.path.join(wabrowser.profile.default_preferences['browser.download.dir'], list(set(newfiles)-set(files))[0]))
                karma.wait(logger=logger, waittime="short")
                # wabrowser.find_element_by_xpath("//div[@title='Close']").click()
                wa_click_element(element="media-close-button", wabrowser=wabrowser, logger=logger)
                karma.wait(logger=logger, waittime="short")
        sender_wa_profile = None
        logger.info("Trying to create profile with dict {}".format(msgdict['sender']))
            # try:
        sender_wa_profile = wa_add_profile_smriti(msgdict['sender'], logger=logger)
        if type(sender_wa_profile) == list and sender_wa_profile != []:
            sender_wa_profile = sender_wa_profile[0]
        # except Exception as e:
        #    logger.error("{} {} trying to add sender profile".format(type(e), str(e)))
        msg = wa_add_message_smriti(msgdict=msgdict, logger=logger)
        if type(msg) == list and msg != []:
            msg = msg[0]
            if sender_wa_profile is not None:
                msg.sent_by = sender_wa_profile
                msg.save()
                msg.reload()
            return msg
    except Exception as e:
        logger.error("{} {}".format(type(e), str(e)))
        return "{} {}".format(type(e), str(e))


def wa_get_message_smriti(msgdict=None, logger=astra.baselogger, **kwargs):
    msgdict2 = deepcopy(msgdict)
    if "files" in msgdict.keys():
        msgdict2.pop("files")
    logger.info("Trying to get message with dict {}".format(msgdict2))
    try:
        msg = wasmriti.WhatsappMessage.objects(**msgdict2)
        return list(msg)
    except Exception as e:
        logger.error("{} {} trying to get message with dict {}".format(type(e), str(e), msgdict))
        return "{} {} trying to get message dict {}".format(type(e), str(e), msgdict)


def wa_add_message_smriti(msgdict=None, logger=astra.baselogger, **kwargs):
    logger.info("Trying to add message with dict {}".format(msgdict))
    try:
        msg = wa_get_message_smriti(msgdict=msgdict, logger=logger)
        if len(msg) and type(msg) != str:
            return list(msg)
        else:
            msg = wasmriti.WhatsappMessage(**msgdict)
            msg.save()
            msg.reload()
            return [msg]
    except Exception as e:
        logger.error("{} {} trying to get message with dict {}".format(type(e), str(e), msgdict))
        return "{} {} trying to get message dict {}".format(type(e), str(e), msgdict)


def wa_export_message_smriti(msgdict=None, path=None, logger=astra.baselogger, **kwargs):
    logger.info("Trying to add message with dict {}".format(msgdict))
    try:
        msg = wa_get_message_smriti(msgdict=msgdict, logger=logger)
        if len(msg) and type(msg) != str:
            msgs = [m.to_mongo().to_dict() for m in msg]
        for msg in msgs:
            if "observed_by" in msg.keys():
                msg['observed_by'] = wasmriti.WhatsappProfile.objects.with_id(msg['observed_by']).naam
            if "observed_in" in msg.keys():
                msg['observed_in'] = wasmriti.WhatsappConversation.objects.with_id(msg['observed_in']).display_name
            msg['_id'] = str(msg['_id'])
            for key in msg.keys():
                if "timestamp" in key:
                    msg[key] = aadhaar.get_local_ts(msg[key])
        msgdf = pandas.DataFrame(msgs)
        msgdf.to_csv(os.path.join(path, "msgreport.csv"), encoding="utf-8")
        return os.path.join(path, "msgreport.csv")
    except Exception as e:
        logger.error("{} {}".format(type(e), str(e)))
        return "{} {}".format(type(e), str(e))


def wa_get_cur_conv_messages(historical=False, scrolls=2, wabrowser=None, logger=astra.baselogger, **kwargs):
    convpane = wa_get_element("convpane", wabrowser=wabrowser, logger=logger)
    scrolled = 0
    lines = []
    msgs = []
    while True:
        numlines = len(lines)
        wabrowser.execute_script("arguments[0].scrollTo(0,0)", convpane)
        karma.wait(waittime="long", logger=logger)
        # lines = wabrowser.find_elements_by_class_name("vW7d1")
        lines = wa_get_element("convpane-item", multi=True, wabrowser=wabrowser, logger=logger)
        for line in lines:
            msg = wa_get_message(line=line, wabrowser=wabrowser, logger=logger)
            if msg is not None:
                msgs.append(msg)
        newnumlines = len(lines)
        if historical is not True:
            if scrolled == scrolls:
                break
        if newnumlines == numlines:
            break
        scrolled += 1
    return msgs


def wa_send_text(wabrowser, text, logger=astra.baselogger, **kwargs):
    logger.info("Sending message {}".format(text))
    textfield = wabrowser.find_elements_by_class_name("_2S1VP")
    t = textfield[-1]
    t.click()
    t.send_keys(text)
    t = wabrowser.find_element_by_class_name("_35EW6")
    t.click()
    karma.wait(logger=logger)


def wa_reply_random(wabrowser, logger=astra.baselogger, **kwargs):
    text = os.popen("fortune -o").read().strip()
    text = text + "\n-Xetrapal is Pal-ing you!"
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
