# from selenium import webdriver
# from xetrapal import astra
# from xetrapal import vaahan
# from xetrapal import karma

from . import whatsappkarmas
from . import astra
from . import karma
from bs4 import BeautifulSoup
import os
import datetime


def wa_get_images_for_users(browser, conversations, logger=astra.baselogger):
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


def wa_get_images_from_contacts(browser):
    contact_chat = browser.find_elements_by_class_name("rAUz7")
    for i in range(len(contact_chat)):
        icon = contact_chat[i].find_element_by_tag_name("span")
        chat = icon.get_attribute("data-icon")
        if chat == u'chat':
            contact_chat[i].click()
            print "yes"
            break
        else:
            print "not this"
    return wa_get_images_for_users(browser)


def wa_get_conv_messages(wabrowser, text, historical=True, scrolls=2, logger=astra.baselogger):
    lines = []
    whatsappkarmas.select_conv(wabrowser, text)
    karma.wait()
    pane2 = wabrowser.find_element_by_class_name("_2nmDZ")
    count = 0
    while True:
        numlines = len(lines)
        wabrowser.execute_script("arguments[0].scrollTo(0,0)", pane2)
        lines = wabrowser.find_elements_by_class_name("vW7d1")
        # TODO: Replace with Whatsapp Classmap in Xetrapal
        karma.wait(waittime="long")
        newnumlines = len(lines)
        if historical is not True:
            if count == scrolls:
                break
        if newnumlines == numlines:
            break
        count += 1
    return lines


def wa_get_message(wabrowser, line, logger=astra.baselogger):
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
                if "m" in msgts:
                    msgdict["created_timestamp"] = karma.get_utc_ts(datetime.datetime.strptime(msgts, "%H:%M %p, %m/%d/%Y"))
                else:
                    msgdict["created_timestamp"] = karma.get_utc_ts(datetime.datetime.strptime(msgts, "%H:%M, %m/%d/%Y"))
                msgdict['sender'] = {"platform": "whatsapp"}
                if not karma.engalpha.search(msgsender):
                    msgdict['sender']['mobile_num'] = msgsender.replace(": ", "").replace(" ", "")
                    logger.info("Mobile Num: {}".format(msgdict['sender']))
                else:
                    msgdict['sender']['whatsapp_contact'] = msgsender.replace(": ", "")
                    logger.info("Whatsapp Contact: {}".format(msgdict['sender']))
                msgdict['text_lines'] = [x.replace("'", "") for x in msg.strings]
                try:
                    msgdict['sender']['displayed_sender'] = linebs.find("span", {"class": "RZ7GO"}).text
                    msgdict['displayed_sender_name'] = linebs.find("span", {"class": "_3Ye_R"}).text
                except Exception as e:
                    logger.error("Could not get display name and sender")
                images = message[0].find_all("img")
                if len(images):
                    image = line.find_element_by_tag_name("img")
                    if "blob" in image.get_attribute("src"):
                        image.click()
                        karma.wait()
                        files = os.listdir(wabrowser.profile.default_preferences['browser.download.dir'])
                        wabrowser.find_element_by_xpath("//div[@title='Download']").click()
                        karma.wait(waittime="long")
                        newfiles = os.listdir(wabrowser.profile.default_preferences['browser.download.dir'])
                        logger.info("Downloaded file {}".format(list(set(newfiles)-set(files))[0]))
                        msgdict['file'] = os.path.join(wabrowser.profile.default_preferences['browser.download.dir'], list(set(newfiles)-set(files))[0])
                        karma.wait()
                        wabrowser.find_element_by_xpath("//div[@title='Close']").click()
                        karma.wait()
            if msgdict != {}:
                msgdict['platform'] = "whatsapp"
                logger.info(msgdict)
                return msgdict
        else:
            return "No message in line"
    except Exception as e:
        logger.error("{} {}".format(type(e), str(e)))
        return "{} {}".format(type(e), str(e))


# not giving rxpected output
'''def wa_search_from_contacts(browser,text,logger=astra.baselogger):
    contact_chat=browser.find_elements_by_class_name("rAUz7")
    contact_chat[1].click()
    karma.wait()
    feild=browser.find_element_by_class_name("jN-F5")
    feild.send_keys(text)
    karma.wait()
    people=browser.find_elements_by_class_name("_2wP_Y")
    names = []

    for num in range(len(people)):
      name_div= people[num].find_elements_by_class_name("_3TEwt")
      if len(name_div)!=0:
          name=name_div[0].find_element_by_tag_name("span")
         # name_=name.find_element_by_tag_name("span")
          name_=name.get_attribute("title")
      else:
          name_="not found "+str(num)
    logger.info("adding " + name_+" to list names")
    names.append(name_)
    return names'''
