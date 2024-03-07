import requests
from .model import Post, Profile
import time
from collections import Counter
import re
from bs4 import BeautifulSoup as bs4
from scraper import utils


class Scraper:
    def __init__(self, profile_url, n_connections=1, min_interactions=2):
        """
        Initialize the Scraper class with the profile URL.

        Args:
            profile_url (str): The URL of the profile to scrape.
        """
        self.min_interactions = min_interactions
        self.n_connections = 1
        self.profile_url = profile_url
        self.id = 0
    
    def scrape_posts(self,driver):
        """
        Scrape posts from the profile URL and extract data and shared URLs.

        Returns:
            A list of Post objects containing the scraped data.
        """
        # Send a request to the profile URL
        #response = requests.get(self.profile_url)
        prof_link = self.profile_url + "/recent-activity/"
        driver.get(prof_link)
        print("Scrapping activity of {}".format(prof_link))
        
        driver = utils.scroll_page(driver)
        data, conn_names, driver = utils.extract_post(driver, self.id)
        if data['ids']:
            self.id = data['ids'][-1] +1
        return data, conn_names, driver
    
    def scrape_profile(self):
        """
        Scrape the profile URL and extract profile data.

        Returns:
            A Profile object containing the scraped data.
        """
        # Send a request to the profile URL
        response = requests.get(self.profile_url)
        

    def scrape_conn_posts(self,driver,conn_names, data):
        for profile,count in conn_names.items():
            if count >=self.min_interactions:
                prof_link = profile + "/recent-activity/"
                driver.get(prof_link)
                print("Scraping activity of {}".format(prof_link))
                

                temp_data,conn_names,driver = utils.extract_post(driver,self.id)
                
                url_texts = []
                if temp_data['ids']:
                    self.id = temp_data['ids'][-1]+1
                print("Saved posts for the profile {}".format(prof_link))
                utils.write_json(temp_data)
        utils.write_json(data)
            

