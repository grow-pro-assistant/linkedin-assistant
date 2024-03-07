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
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs4
import re
from collections import Counter
import os
import time
import json
import getpass
from .url_scraper.scraper import Scraper as Url_Scraper
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path

CREDENTIALS_FILE = 'linkedin_data.txt'

def get_url_text(url):
    url_scraper = Url_Scraper(url)
    page = url_scraper.scrape()
    complete_text = page.metadata + '\n' + page.heading + '\n' + page.text 
    print('complete_text', complete_text[:100])
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





def get_credentials_and_profile():
    # Check if data file exists
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as file:
            lines = file.readlines()
            USERNAME, PASSWORD = lines[0].strip().split()
            profile_url = lines[1].strip() if len(lines) > 1 else None
    else:
        USERNAME = input("Enter the username: ")
        PASSWORD = getpass.getpass("Enter the password: ")
        profile_url = None
        
        # Ask user if they want to save the credentials for next time
        save = input("Save credentials for next time? (y/n): ").lower()
        if save == 'y':
            with open(CREDENTIALS_FILE, 'w') as file:
                file.write(f"{USERNAME} {PASSWORD}\n")
    
    return USERNAME, PASSWORD, profile_url

def access_profile():
    USERNAME, PASSWORD, saved_profile_url = get_credentials_and_profile()

    browser = get_browser_info()
    driver = get_driver(browser)
    ## access LinkedIn and login...
    # After successful login and fetching the profile URL:
    url = "https://linkedin.com/"
    driver.get(url)
    wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#session_key")))

    ### sign in to linkedin
    ## input username and password to required fields
    email = driver.find_element(By.CSS_SELECTOR, "#session_key")
    email.send_keys(USERNAME)

    password = driver.find_element(By.CSS_SELECTOR, "#session_password")
    password.send_keys(PASSWORD)

    ## press the login button after entering the details
    login = driver.find_element('css selector','button.btn-primary')
    login.click()

    ### goto profile and then recent activity link
    #get linkedin profile link
    wait = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".feed-identity-module__actor-meta.break-words")))
    own_profile = driver.find_element('css selector','.feed-identity-module__actor-meta.break-words').find_element('css selector','.ember-view.block').get_attribute("href")

    own_profile_link = own_profile
    return own_profile_link, driver




    return USERNAME,PASSWORD

def get_browser_info():
    print("Select your browser")
    browser = input("Press 'f' for Firefox \n 'c' for Google Chrome and \n 'e' for Microsoft Edge \n Your Selection: ")    
    return browser



    

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
        return webdriver.Firefox(options=options)
    elif browser == "c":
        options = ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        options.add_argument('--disable-logging')
        options.add_argument("--disable-blink-features=AutomationControlled")
        print("binary path", binary_path)
        svc = webdriver.ChromeService(executable_path=binary_path)
        driver = webdriver.Chrome(service=svc, options=options)
        return driver
    elif browser == "e":
        options = EdgeOptions()
        return webdriver.Edge(options=options)
    else:
        options = Options()
        options.add_argument("--incognito")
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        return webdriver.Firefox(options=options)



# def scroll_page(driver):
#     #### getting posts that are gathered in 20 seconds of scroll
#     start=time.time()
#     n =3
#     lastHeight = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(1)
#         newHeight = driver.execute_script("return document.body.scrollHeight")
#         if newHeight == lastHeight:
#             break
#         lastHeight = newHeight
#         end=time.time()
#         if round(end-start)>n:
#             break

#     return driver

def scroll_page(driver, max_duration='4mo'):
    print('scrolling page')
    start = time.time()
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    
    # This selector needs to be updated based on the actual structure of the webpage
    time_class = ".update-components-actor__sub-description.t-12.t-normal"
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Let the page load
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            print("Reached the end of the page.")
            break
        lastHeight = newHeight
        

        try:
            # Assuming the timestamps are visible and accessible
            # This will get the last post's timestamp text
            last_post_time = driver.find_elements(By.CSS_SELECTOR, time_class)[-1].text.strip().split('•')[0]
            print('last_post_time:', last_post_time)
            
            # Call the compare_times function to decide whether to stop scrolling
            if compare_times(last_post_time, max_duration):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                last_post_time = driver.find_elements(By.CSS_SELECTOR, time_class)[-1].text.strip().split('•')[0]
                print('last_post_time:', last_post_time)
                if compare_times(last_post_time, max_duration):
                    print("Reached the end of the relevant posts.")
                    break
        except NoSuchElementException:
            print("Timestamp element not found, ensure the selector is correct.")
            break  # If we can't find the timestamp, stop to avoid an infinite loop

    return driver


# def scroll_page(driver):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def extract_post(driver, id):
    conn_names = Counter()
    data = {"ids": [], "p_text": [], "urls": [], "actor": [], "time":[], 'url_texts': []}

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".profile-creator-shared-feed-update__container")))

    # Find all buttons for filtering posts (if any)
    buttons = driver.find_elements(By.CSS_SELECTOR, ".profile-creator-shared-pills__pill.artdeco-pill.artdeco-pill--slate.artdeco-pill--choice.artdeco-pill--3.artdeco-pill--toggle")
    if buttons:
        for button in buttons:
            if button.text not in ['Posts', 'Comments', 'Reactions', 'More']:
                print('skipping button:', button.text)
                continue
            print('scrapping posts for', button.text)
            
            # Scroll to the button
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
            try:
                driver.execute_script("window.scrollTo(0, 0);")
                button.click()
            except  Exception as e:
                print(f"Error clicking button: {e}")
                # Use JavaScript click as a fallback
                print('using alternate click')
                driver.execute_script("arguments[0].click();", button)
            if button.text == 'More':
                # sub_buttons = driver.find_elements(By.CSS_SELECTOR, "artdeco-dropdown__content-inner")
                sub_buttons = driver.find_elements(By.CSS_SELECTOR, ".artdeco-dropdown__item.artdeco-dropdown__item--is-dropdown.ember-view")
                for sub_button in sub_buttons:
                    if sub_button.text in  ['Posts', 'Comments', 'Reactions']:
                        sub_button.click()
                        data, conn_names, id, driver = extract_post_page(data, conn_names, id, driver, sub_button)
            else:
                data, conn_names, id, driver =  extract_post_page(data, conn_names, id, driver, button)
    else:
        data, conn_names, id, driver = extract_post_page(data, conn_names, id, driver, None)
    scrape_urls(data)
    print("Total number of posts extracted:", len(data["p_text"]))

    return data, conn_names, driver

def extract_post_page(data, conn_names, id, driver, button):
    # Wait for the page to load
    try:
        post_visbility_class = ".profile-creator-shared-feed-update__container"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, post_visbility_class)))
    except NoSuchElementException:
        print(f"Element with CSS selector '{post_visbility_class}' not found on the page.")
        return data, conn_names, id, driver
    scroll_page(driver)
    try:
        # Wait for the "ember-view occludable-update" class to appear
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ember-view.occludable-update")))
        containers = driver.find_elements(By.CSS_SELECTOR, ".feed-shared-update-v2.feed-shared-update-v2--minimal-padding.full-height.relative.artdeco-card")
        for container in containers:
            success = extract_data_from_container(container, data, conn_names, id)
            if success:
                id += 1
    except  Exception as e:
        print(f"Error processing extract_post_page: {e}")
        if button:
            print("No posts found for this section",  button.text)
        else:
            print("No posts found")
        data, conn_names, id, driver
    return data, conn_names, id, driver

def extract_data_from_container(container, data, conn_names, id):
    # Initialize temporary data dictionary
    temp_data = {"actor": "", "p_text": "", "urls": [], "ids": id, "time": ""}
    
    try:
        # Get poster's name
        name_box = container.find_element(By.CSS_SELECTOR, ".update-components-actor__meta a")
        actor_name = name_box.get_attribute("href").split("?")[0]
        conn_names[actor_name] += 1
        temp_data["actor"] = actor_name
        time_class = ".update-components-actor__sub-description.t-12.t-normal"
        temp_data["time"] = container.find_element(By.CSS_SELECTOR, time_class).text.strip().split('•')[0]
                

        # Get post text
        text_box_class = ".update-components-text.relative.update-components-update-v2__commentary span[dir='ltr']"
        text_box = container.find_element(By.CSS_SELECTOR, text_box_class)
        if text_box is None:
            return False
        post_text = text_box.text.strip()
        temp_data["p_text"] = post_text

        # Extract URLs from post text
        post_urls = re.findall(r"https?://[^\s]+", post_text)
        temp_data["urls"] = post_urls
        print('actor:', temp_data["actor"])
        print('post_text:', temp_data["p_text"][:15])
        print('urls:', temp_data["urls"])
        print('time:', temp_data["time"])

        # Add temporary data to main data dictionary
        for key, value in temp_data.items():
            data[key].append(value)
        return True
    except NoSuchElementException:
        print(f"Element with CSS selector '{text_box_class}' not found on the page.")
        return False
    
def parse_time_expression(time_expression):
    """
    Parse a time expression and convert it to a uniform format in hours.
    Handles different units of time (hours, days, weeks, months, years)
    and accounts for singular and plural forms, as well as different abbreviations.
    """
    # Dictionary to map time units to their respective multipliers (in hours)
    time_units = {
        'h': 1,          # Hour
        'hr': 1,         # Hour (alternative abbreviation)
        'd': 24,         # Day
        'w': 24 * 7,     # Week
        'mo': 24 * 30,   # Month (approximated as 30 days)
        'month': 24 * 30,# Month (alternative spelling)
        'yr': 24 * 365,  # Year
        'year': 24 * 365 # Year (alternative spelling)
    }

    # Regular expression to match the time expression format
    match = re.match(r"(\d+)\s*([a-zA-Z]+)", time_expression)
    if not match:
        return 0  # Return 0 hours if the format is incorrect or not recognized

    magnitude, unit = match.groups()
    magnitude = int(magnitude)
    unit = unit.lower()  # Convert unit to lowercase to match dictionary keys

    # Handle plural forms and different abbreviations by finding the closest match in the dictionary
    if unit.endswith('s'):  # Remove plural 's' for simplicity
        unit = unit[:-1]
    if unit in time_units:
        return magnitude * time_units[unit]
    else:
        # If the unit is not recognized, return 0
        return 0

def compare_times(time1, time2):
    """
    Compare two time expressions.
    Each time expression should be in a format that parse_time_expression can understand.
    Returns True if time1 is greater than or equal to time2, otherwise False.
    """
    total_hours1 = parse_time_expression(time1)
    total_hours2 = parse_time_expression(time2)

    return total_hours1 >= total_hours2

def scrape_urls(data):
    # Extract text from URLs and append to 'url_texts'
    url_texts = []
    for post_urls in data['urls']:
        post_texts = []
        for url in post_urls:
            post_texts.append(get_url_text(url))
        url_texts.append('\n'.join(post_texts))
    
    data['url_texts']+=url_texts



def extract_pos1(driver,id):
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
        print("length of containers",len(containers))
        for container in containers:
            if container is None:
                print("None")
            # try:
            elements = container.find_elements(By.CSS_SELECTOR, '*')
            if len(elements) == 0:
                continue
            #print legnth of elements
            print("legnth of elements", len(elements))

            # try:
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
            # except:
            #     for element in elements:
            #         class_attr = element.get_attribute('class')
            #         if class_attr:
            #             print(f"Element with class attribute '{class_attr}':")
            #             print(f"CSS Selector: .{class_attr.replace(' ', '.')}")
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
            f"time": data["time"][i],
            f"url_links": data["urls"][i],
            f"url_texts": data["url_texts"][i],
        }

        json_objects.append(entry)

    # Write the scraped data to a JSON file
    with open("scraped_data.json", "w", encoding="utf-8") as outfile:
        json.dump(json_objects, outfile, ensure_ascii=False, indent=4)
