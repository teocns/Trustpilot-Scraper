import constants
import os
from helpers import get_all_categories
from proxy_chrome import proxy_chrome
from proxy_handler import ProxyHandler
from time import sleep
from contextlib import nullcontext

import requests


# Get all categories
categories = get_all_categories(1)


proxy_handler = ProxyHandler()




XPATH_TO_FIND_MORE_SUBCATEGORIES = """//*[@id="__next"]/div/main/div/div[2]/aside/div[1]/div/div[2]/div/ul"""
THREADS = 4


def testCategory(category):
    proxy = proxy_handler.getProxy()
    print(f"Using proxy {proxy.ip} for category {category['name']}")
    browser =  proxy_chrome(proxy.ip, proxy.port, proxy.user, proxy.password)
    browser.get(category['url'])
    element_found = browser.find_elements_by_xpath(XPATH_TO_FIND_MORE_SUBCATEGORIES)

    
    if element_found:
        el = element_found[0]
        
        subels = el.find_elements_by_css_selector('ul li a')
        print('Found sub elements: '+str(len(subels)))
        for subel in subels:
            href = subel.get_attribute('href')
            if '/categories/' in href:
                href = href.strip().strip("#")
                try:
                    category_name = str(browser.execute_script('return arguments[0].querySelector("span").innerText',subel))
                except:
                    continue
                if not category_name:
                    continue
                if category_name.find('('):
                    category_name = category_name[0:category_name.find('(')].strip()
                
                result = requests.post(
                    constants.ENDPOINT,
                    json={
                        "action":"store_category",
                        "category":{
                            "url":href,
                            "name":category_name,
                            "parent_id":category['id'],
                            "hierarchy_index":2
                        }
                    }
                )
                print(result.text)
    else:
        print(f"Not found {category['url']}")
        
    browser.quit()

#testCategory(categories[0])
from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool(4)

pool.map(testCategory,categories)
        
