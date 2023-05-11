import requests
from .model import Post, Profile
import time
from collections import Counter
import re
from bs4 import BeautifulSoup as bs4
from scraper import utils


class Scraper:
    def __init__(self, profile_url, n_connections=1, min_interactions=1):
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

        url_texts = []
        for post_urls in data['urls']:
            post_texts = []
            for url in post_urls:
                post_texts.append(utils.get_url_text(url))
            url_texts.append('\n'.join(post_texts))

        data['url_texts'] = url_texts
        self.id = data['ids'][-1]
        utils.write_json(data ,max_id=self.id)
        return data, conn_names, driver
# =======

# #         for post_urls in urls:
# #            post_texts = []
# #            for url in post_urls:
# #                post_texts.append(utils.get_url_text(url))
# #             url_texts.append('\n'.join(post_texts))
#         if ids:
#             self.id = ids[-1]+1
#         utils.write_json(ids,p_text,actor,urls, url_texts,max_id=self.id)
#         return ids,p_text,actor,urls,conn_names,driver, url_texts
# >>>>>>> organization/scraper
    
    def scrape_profile(self):
        """
        Scrape the profile URL and extract profile data.

        Returns:
            A Profile object containing the scraped data.
        """
        # Send a request to the profile URL
        response = requests.get(self.profile_url)
        
        # Parse the response and extract profile data
        # ...
        
        # Create a Profile object and return it
        # ...


    def scrape_conn_posts(self,driver,conn_names):
        for profile,count in conn_names.items():
            if count >=self.min_interactions:
                prof_link = profile + "/recent-activity/"
                driver.get(prof_link)
                print("Scrapping activity of {}".format(prof_link))
                

                driver = utils.scroll_page(driver)
                data,conn_names,driver = utils.extract_post(driver,self.id)
                
                url_texts = []

                for post_urls in data['urls']:
                    post_texts = []
                    for url in post_urls:
                        post_texts.append(utils.get_url_text(url))
                    url_texts.append('\n'.join(post_texts))
                data['url_texts'] = url_texts
                #print(ids)
                if data['ids']:
                    self.id = data['ids'][-1]
                utils.write_json(data,max_id=self.id)
                print("Saved posts for the profile {}".format(prof_link))
            

