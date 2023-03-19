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
    signInButton = driver.find_element(By.XPATH,"/html/body/main/section[1]/div/form[1]/div[2]/button")
    signInButton.click()

    ## input username and password to required fields
    email = driver.find_element(By.XPATH,'//*[@id="session_key"]')
    email.send_keys(USERNAME)

    password = driver.find_element(By.XPATH,'//*[@id="session_password"]')
    password.send_keys(PASSWORD)

    ## press the login button after entering the details
    login = driver.find_element(By.XPATH,'/html/body/main/section[1]/div/form[1]/div[2]/button')
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