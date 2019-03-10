# coding: utf-8
import time
import datetime
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
'''
यहां हम फेसबुक सम्बन्धी अस्त्रों का उल्लेख करेंगे
'''
# from .astra import *
from . import astra
from . import karma

# Fire and Forget Astras, to be run with {'msg':'run','func':function_object,'args':(),'kwargs':{}}


def fb_login(browser, config=None, logger=astra.baselogger, **kwargs):
    fbusr = config.get("Facebook", "fbusername")
    fbpwd = config.get("Facebook", "fbpassword")
    # or you can use Chrome(executable_path="/usr/bin/chromedriver")
    logger.info("Trying to log into FB in browser...")
    try:
        browser.get("http://www.facebook.com")
        assert "Facebook" in browser.title
        elem = browser.find_element_by_id("email")
        elem.send_keys(fbusr)
        elem = browser.find_element_by_id("pass")
        elem.send_keys(fbpwd)
        elem.send_keys(Keys.RETURN)
        time.sleep(10)
        browser.get("http://facebook.com/profile.php")
        time.sleep(10)
        logger.info("Successfully logged into FB")
    except Exception as exception:
        logger.error("Could not log into FB.." + repr(exception))


def fb_search(fbbrowser, searchstring, logger=astra.baselogger, **kwargs):
    logger.info("Searching FB for " + searchstring)
    searchbar = fbbrowser.find_element_by_name("q")
    searchbar.clear()
    searchbar.send_keys(searchstring)
    searchbar.send_keys(Keys.ENTER)
    time.sleep(10)


def fb_get_posts_from_timeline(fbbrowser, url="https://facebook.com", count=10, logger=astra.baselogger, **kwargs):
    fbbrowser.get(url)
    karma.wait()
    postlinks = []

    while len(postlinks) < count:
        posts = []
        postcontents = []
        posts = posts + \
            fbbrowser.find_elements_by_class_name("userContentWrapper")
        for post in posts:
            postcontents.append(BeautifulSoup(post.get_property("innerHTML")))
        for postcontent in postcontents:
            pc = list(postcontent.find_all("a", {"class": "_5pcq"}))
            if len(pc) > 0:
                pc = pc[0]
            else:
                continue
            url = "https://facebook.com" + pc.get("href")
            logger.info("Logging post at {}".format(
                pc.find("abbr").get("title")))
            postlink = {}
            postlink['text'] = postcontent.text
            postlink['url'] = url
            postlink['timestamp'] = datetime.datetime.strptime(
                pc.find("abbr").get("title"), "%d/%m/%Y, %H:%M")
            if url not in [pl['url'] for pl in postlinks]:
                postlinks.append(postlink)
        logger.info("Got %s posts " % (len(postlinks)))
        # postlinks = list(set(postlinks))
        if "https://facebook.com#" in postlinks:
            postlinks.pop(postlinks.index("https://facebook.com#"))
        karma.scroll_page(fbbrowser)
        karma.wait()
    return postlinks[:count]


def fb_get_profile_data(fbbrowser, url, logger=astra.baselogger, **kwargs):
    profiledata = {}
    profilepic = {}
    fbbrowser.get(url)
    karma.wait()
    profile = fbbrowser.current_url

    if profile == "http://www.facebook.com/profile.php":
        plink = fbbrowser.find_element_by_xpath("//a[@title='Profile']")
        profile = plink.get_attribute("href")

    profiledata['url'] = profile
    # plink=fbbrowser.find_element_by_xpath("//a[@title='Profile']")

    profiledata['fbdisplayname'] = fb_get_cur_page_displayname(fbbrowser)

    fbbrowser.find_element_by_class_name("profilePic").click()
    time.sleep(10)
    '''
    try:
        profilepic['alttext'] = fbbrowser.find_element_by_class_name(
            "spotlight").get_property("alt")
        profilepic['src'] = fbbrowser.find_element_by_class_name(
            "spotlight").get_property("src")
        profilepic['profileguard'] = False
    except Exception as e:
        logger.error("{} {}".format(type(e), str(e)))
        profilepic['alttext'] = fbbrowser.find_element_by_class_name(
            "profilePicThumb").get_property("alt")
        profilepic['src'] = fbbrowser.find_element_by_class_name(
            "profilePic").get_property("src")
        profilepic['profileguard'] = True
    try:
        localfile = karma.download_file(
            profilepic['src'], prefix=profiledata['fbdisplayname'].replace(" ", ""), suffix=".jpg")
        profilepic['localfile'] = localfile

    except Exception as e:
        logger.error("Failed to download {} {}".format(type(e), str(e)))
    '''
    profiledata['tabdata'] = fb_get_profile_tab_data(fbbrowser, url)
    profiledata['friendcount'] = profiledata['tabdata']['friends']['count']
    profiledata['profilepic'] = profilepic
    return profiledata


def fb_get_profile_tab_data(fbbrowser, profileurl, **kwargs):
    tabdata = {"friends": {}, "photos": {}, "about": {}}
    fbbrowser.get(profileurl)
    time.sleep(5)
    phototab = fbbrowser.find_element_by_xpath(
        "//a[@data-tab-key='photos']").get_property("href")
    friendtab = fbbrowser.find_element_by_xpath(
        "//a[@data-tab-key='friends']").get_property("href")
    abouttab = fbbrowser.find_element_by_xpath(
        "//a[@data-tab-key='about']").get_property("href")
    tabdata['friends']['url'] = friendtab
    if fbbrowser.find_element_by_xpath("//a[@data-tab-key='friends']").get_property("text").replace("Friends", "") != "" and "Mutual" not in fbbrowser.find_element_by_xpath("//a[@data-tab-key='friends']").get_property("text"):
        tabdata['friends']['count'] = int(fbbrowser.find_element_by_xpath(
            "//a[@data-tab-key='friends']").get_property("text").replace("Friends", ""))
    else:
        tabdata['friends']['count'] = -1
    tabdata['photos']['url'] = phototab
    tabdata['about']['url'] = abouttab
    return tabdata


def fb_get_cur_page_displayname(fbbrowser, **kwargs):
    displayname = fbbrowser.find_element_by_id(
        "fb-timeline-cover-name").find_element_by_tag_name("a").text
    return displayname


def fb_like_page_toggle(fbbrowser, pageurl, **kwargs):
    fbbrowser.get(pageurl)
    likebutton = fbbrowser.find_element_by_xpath(
        "//button[@data-testid='page_profile_like_button_test_id']")
    likebutton.click()
