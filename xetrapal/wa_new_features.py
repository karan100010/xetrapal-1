from selenium import webdriver
from xetrapal import astra
from xetrapal import vaahan
from xetrapal import karma
from xetrapal import whatsappkarmas


def wa_get_images_for_users(browser,logger=astra.baselogger):
    people = browser.find_elements_by_class_name("_2wP_Y")
    names = []
    image_list=[]
    for conv in range(len(conversations)):
     name_div= conversations[conv].find_elements_by_class_name("_3TEwt")
     if len(name_div)!=0:
         name=name_div[0].find_element_by_tag_name("span")
        # name_=name.find_element_by_tag_name("span")

         name_=name.get_attribute("title")
     else:
         name_="not found "+str(conv)
     logger.info("adding " + name_+" to list names")
     names.append(name_)
    for i in range(len(conversations)):
              image_div=conversations[i].find_elements_by_class_name("_1WliW")
              if len(image_div)!=0:
                   image_tag=image_div[0].find_elements_by_tag_name("img")
              else :

                   image_tag=[]
                   i+1
              if len(image_tag)!=0:
                  link=image_tag[0].get_attribute("src")
                  if "https" not in link:
                      link="not found"
              else :
                  link="not found"

              logger.info("adding " + link+" to image list")
              image_list.append(link)
    dic=dict(zip(names,image_list))
    return dic
#a=get_images_for_users(browser)\

def wa_get_images_from_contacts(browser):
    contact_chat=browser.find_elements_by_class_name("rAUz7")
    for i in range(len(contact_chat)):
     icon=contact_chat[i].find_element_by_tag_name("span")
     chat= icon.get_attribute("data-icon")
     if chat==u'chat':
        contact_chat[i].click()
        print "yes"
        break
     else:
        print "not this"
    return wa_get_images_for_users(browser)
#not giving rxpected output
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
