import re
import requests
### Importing required libraries
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs4
import re
from collections import Counter
import os
import time
import json
import getpass
from .url_scraper.scraper import Scraper as Url_Scraper

def get_url_text(url):
    url_scraper = Url_Scraper(url)
    page = url_scraper.scrape()
    complete_text = page.metadata + '\n' + page.heading + '\n' + page.text 
    return complete_text

def extract_shared_urls(text):
    """
    Extract shared URLs from a given text.

    Args:
        text (str): The text to extract URLs from.

    Returns:
        A list of URLs found in the text.
    """
    # Use regularexpressions to extract URLs from the text
    # ...

def crawl_url(url):
    """
    Crawl a given URL and extract paragraphs and headings.
    Args:
        url (str): The URL to crawl.

    Returns:
        A dictionary containing the crawled data.
    """
    # Send a request to the URL
    response = requests.get(url)

    # Parse the response and extract paragraphs and headings
    # ...

    # Create a dictionary and return it
    # ...

def get_profile():
    USERNAME,PASSWORD = get_credentials()
    profile_url, driver = access_profile(USERNAME,PASSWORD)

    return profile_url, driver



def get_credentials():
    USERNAME = input("Enter the username: ")
    # USERNAME = 'xxxxxxx'
    PASSWORD = getpass.getpass()
    # PASSWORD = 'xxxxxxx'


    return USERNAME,PASSWORD

def get_browser_info():
    print("Select your browser")
    browser = input("Press 'f' for Firefox \n 'c' for Google Chrome and \n 'e' for Microsoft Edge \n Your Selection: ")    
    return browser

def access_profile(USERNAME,PASSWORD):

    browser = get_browser_info()
    driver = get_driver(browser)
    ## access linkedin
    url = "https://linkedin.com/"
    driver.get(url)
    wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#session_key")))

    ### sign in to linkedin
 #   signInButton = driver.find_element(By.XPATH,"/html/body/main/section[1]/div/form[1]/div[2]/button")
 #   signInButton.click()
#/html/body/main/section[1]/div/div/form/div[2]/button
    ## input username and password to required fields
    email = driver.find_element(By.CSS_SELECTOR, "#session_key")
    email.send_keys(USERNAME)

    password = driver.find_element(By.CSS_SELECTOR, "#session_password")
    password.send_keys(PASSWORD)

    ## press the login button after entering the details
    #login = driver.find_element(By.XPATH,'/html/body/main/section[1]/div/div/form/div[2]/button')
    login = driver.find_element('css selector','button.btn-primary')
    login.click()

    ### goto profile and then recent activity link
    #get linkedin profile link
    wait = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".feed-identity-module__actor-meta.break-words")))
    own_profile = driver.find_element('css selector','.feed-identity-module__actor-meta.break-words').find_element('css selector','.ember-view.block').get_attribute("href")

    ##profile = driver.find_element(By.CSS_SELECTOR,'div.t-16:nth-child(2)')
    # own_profile.click()
    own_profile_link = own_profile

    return own_profile_link,driver

    


    

def get_driver(browser):
    """
    Returns a Selenium WebDriver instance based on the specified browser type.

    Args:
        browser (str): The browser type (f for Firefox, c for Chrome, e for Edge).

    Returns:
        WebDriver: A Selenium WebDriver instance for the specified browser.
    """
    if browser == "f":
        options = Options()
        options.add_argument("--incognito")
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        return webdriver.Firefox(options=options, executable_path=r"..\driver\geckodriver.exe")
    elif browser == "c":
        options = ChromeOptions()
        return webdriver.Chrome(options=options)
    elif browser == "e":
        options = EdgeOptions()
        return webdriver.Edge(options=options)
    else:
        options = Options()
        options.add_argument("--incognito")
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        return webdriver.Firefox(options=options, executable_path=r"..\driver\geckodriver.exe")



def scroll_page(driver):
    #### getting posts that are gathered in 20 seconds of scroll
    start=time.time()
    n =3
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight
        end=time.time()
        if round(end-start)>n:
            break

    return driver

def extract_post(driver,id):
    # extract post data
    # ...
    wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ember-view.occludable-update")))
    buttons = driver.find_elements(By.CLASS_NAME, "profile-creator-shared-pills__pill.artdeco-pill.artdeco-pill--slate.artdeco-pill--choice.artdeco-pill--3.artdeco-pill--toggle")
    # Click on each button and wait for the "ember-view occludable-update" class to appear
    containers = []  
    conn_names = Counter()
    data = {"ids": [], "p_text": [], "urls": [], "actor": [], 'url_texts': []}
    for button in buttons:
        button.click()
        try:
            # check if there exists any entry/post under section
            wait = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".profile-creator-shared-feed-update__container")))
        except:
            continue
        scroll_page(driver)
        #get first div under the post html 
        containers  =  driver.find_elements(By.CSS_SELECTOR, ".feed-shared-update-v2.feed-shared-update-v2--minimal-padding.full-height.relative.artdeco-card")
        print(len(containers))
        for container in containers:
            if container is None:
                print("None")
            # try:
            elements = container.find_elements(By.CSS_SELECTOR, '*')
            if len(elements) == 0:
                continue
            #print legnth of elements
            print(len(elements))

            try:
                # Add ID to data
                data["ids"].append(id)

                # Get poster's name
                name_box = container.find_element(By.CSS_SELECTOR, ".app-aware-link.update-components-actor__container-link.relative.display-flex.flex-grow-1")
                name = name_box.get_attribute("href").split("?")[0]
                conn_names[name] += 1
                data["actor"].append(name)
                print('name', name)

                # Get post text
                text_box = container.find_element(By.CSS_SELECTOR, ".update-components-text.relative.feed-shared-update-v2__commentary")
                text = text_box.find_element(By.CSS_SELECTOR, "span[dir='ltr']")
                post_text = text.text.strip()
                print('post_text:', post_text[:15]  )
                data["p_text"].append(post_text)

                # Extract URLs from post text
                if "https" in post_text:
                    post_urls = re.findall("(?P<url>https?://[^\s]+)", post_text)
                else:
                    post_urls = []
                data["urls"].append(post_urls)

                ## increment id
                id = id+1
                # except:
                #     continue
            except:
                for element in elements:
                    class_attr = element.get_attribute('class')
                    if class_attr:
                        print(f"Element with class attribute '{class_attr}':")
                        print(f"CSS Selector: .{class_attr.replace(' ', '.')}")
    if not buttons:
        try:
            # check if there exists any entry/post under section
            wait = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".profile-creator-shared-feed-update__container")))
        except:
            return data, conn_names, driver
        scroll_page(driver)
        #get first div under the post html 
        containers  =  driver.find_elements(By.CSS_SELECTOR, ".feed-shared-update-v2.feed-shared-update-v2--minimal-padding.full-height.relative.artdeco-card")
        print(len(containers))
        for container in containers:
            if container is None:
                print("None")
            elements = container.find_elements(By.CSS_SELECTOR, '*')
            if len(elements) == 0:
                continue
            #print legnth of elements
            print(len(elements))
            try:
                # Add ID to data
                data["ids"].append(id)

                # Get poster's name
                name_box = container.find_element(By.CSS_SELECTOR, ".app-aware-link.update-components-actor__container-link.relative.display-flex.flex-grow-1")
                name = name_box.get_attribute("href").split("?")[0]
                conn_names[name] += 1
                data["actor"].append(name)
                print('name', name)

                # Get post text
                text_box = container.find_element(By.CSS_SELECTOR, ".update-components-text.relative.feed-shared-update-v2__commentary")
                text = text_box.find_element(By.CSS_SELECTOR, "span[dir='ltr']")
                post_text = text.text.strip()
                print('post_text:', post_text[:15]  )
                data["p_text"].append(post_text)

                # Extract URLs from post text
                if "https" in post_text:
                    post_urls = re.findall("(?P<url>https?://[^\s]+)", post_text)
                else:
                    post_urls = []
                data["urls"].append(post_urls)

                ## increment id
                id = id+1
            except:
                for element in elements:
                    class_attr = element.get_attribute('class')
                    if class_attr:
                        print(f"Element with class attribute '{class_attr}':")
                        print(f"CSS Selector: .{class_attr.replace(' ', '.')}")
    print("total number of posts are: ", len(data["p_text"]))
    print("total number of urls are: ", len(data["urls"]) - data["urls"].count(""))
    print("interacted with whom", conn_names)


    url_texts = []
    for post_urls in data['urls']:
        post_texts = []
        for url in post_urls:
            post_texts.append(get_url_text(url))
        data['url_texts'].append('\n'.join(post_texts))
    return data, conn_names, driver



def write_json(data):
    json_objects = []
    
    for i in range(len(data["p_text"])):
        entry = {
            f"id": data["ids"][i],
            f"person_name": data["actor"][i],
            f"text_description": data["p_text"][i],
            f"url_links": data["urls"][i],
            f"url_texts": data["url_texts"][i],
        }

        json_objects.append(entry)

    # Write the scraped data to a JSON file
    with open("scraped_data.json", "w", encoding="utf-8") as outfile:
        json.dump(json_objects, outfile, ensure_ascii=False, indent=4)
