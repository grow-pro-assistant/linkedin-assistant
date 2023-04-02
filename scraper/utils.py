import re
import requests
### Importing required libraries
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4
import re
from collections import Counter
import os
import time
import json

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
    PASSWORD = input("Enter the password: ")

    return USERNAME,PASSWORD

def access_profile(USERNAME,PASSWORD):

    driver = get_driver()
    ## access linkedin
    url = "https://linkedin.com/"
    driver.get(url)
    time.sleep(2)

    ### sign in to linkedin
 #   signInButton = driver.find_element(By.XPATH,"/html/body/main/section[1]/div/form[1]/div[2]/button")
 #   signInButton.click()
#/html/body/main/section[1]/div/div/form/div[2]/button
    ## input username and password to required fields
    email = driver.find_element(By.XPATH,'//*[@id="session_key"]')
    email.send_keys(USERNAME)

    password = driver.find_element(By.XPATH,'//*[@id="session_password"]')
    password.send_keys(PASSWORD)

    ## press the login button after entering the details
    login = driver.find_element(By.XPATH,'/html/body/main/section[1]/div/div/form/div[2]/button')
    login.click()

    ### goto profile and then recent activity link
    own_profile = driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div/div[2]/div/div/div/div[1]/div[1]/a/div[2]')
    ##profile = driver.find_element(By.CSS_SELECTOR,'div.t-16:nth-child(2)')
    own_profile.click()

    own_profile_link = driver.current_url

    return own_profile_link,driver

    


    

def get_driver():
    ### browser params for selenium
    firefox_options = Options()
    firefox_options.add_argument("--incognito")
    firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe' ## give firefox exe path here

    ### running the webdriver
    driver = webdriver.Firefox(options=firefox_options, executable_path=r"..\driver\geckodriver.exe") ## path where driver is present

    return driver

def scroll_page(driver):
    #### getting posts that are gathered in 20 seconds of scroll
    start=time.time()
    n =20
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
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
    posts_source = driver.page_source 
    linkedin_soup = bs4(posts_source.encode("utf-8"), "html")
    linkedin_soup.prettify()
    containers = linkedin_soup.findAll("div",{"class":"ember-view occludable-update"})
    conn_names = Counter()
    p_text,urls,actor,ids =[],[],[],[]
    for container in containers:

        try:
            ids.append(id)
            ## get poster's name
            name_box = container.find("div",{"class":"update-components-actor"})
            name = name_box.find("a")['href'].split("?")[0]
            #name  = name.text.strip()
            actor.append(name)
            conn_names.update([name])

            ## get post text  
            text_box = container.find("div",{"class":"feed-shared-update-v2__description-wrapper"})
            text = text_box.find("span",{"dir":"ltr"})
            post_text = text.text.strip()
            p_text.append(post_text)
            #print(post_text)

            ## extract urls
            if "https" in post_text:
                post_url = re.findall("(?P<url>https?://[^\s]+)", post_text)
            else:
                post_url = ""
            #print(post_url)
            urls.append(post_url)

            ## increment id
            id = id+1

        except:
            #print(text_box)
            pass
    print("total number of posts are: ",len(p_text))
    print("total number of urls are: ",len(urls)-urls.count(""))
    print("interacted with whom",conn_names)
    return ids,p_text,actor,urls,conn_names,driver


def write_json(ids,posts,actors,urls):
    json_objects={}

    for i in range(len(posts)):

        entry = {f"id{i}": ids[i], f"person_name{i}": actors[i], f"text_description{i}": posts[i], f"url_links{i}": urls[i]}

        json_objects.update(entry)


    ## Write the scraped data to a JSON file
    out_json("scraped_data.json",json_objects)


def out_json(fname,data):
    if os.path.exists(fname):
    #read existing file and append new data
        with open(fname,"r") as f:
            loaded = json.load(f)
        ##loaded.append({'appended': time.time()})
        loaded.append(data)
    else:
        #create new json
        loaded = [data]

    #overwrite/create file
    with open(fname,"w") as f:
        json.dump(loaded,f)