import requests
from .model import Post, Profile

class Scraper:
    def __init__(self, profile_url, n_connections=1, min_interactions=3):
        """
        Initialize the Scraper class with the profile URL.

        Args:
            profile_url (str): The URL of the profile to scrape.
        """
        self.min_interactions = min_interactions
        self.n_connections = 1
        self.profile_url = profile_url
    
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
        print("Scrapping activity of {}".format(profile))
        #### getting posts that are gathered in 20 seconds of scroll
        start=time.time()
        n =200
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



        # Parse the response and extract post data
        # ...
        posts_source = driver.page_source 
        linkedin_soup = bs4(posts_source.encode("utf-8"), "html")
        linkedin_soup.prettify()
        containers = linkedin_soup.findAll("div",{"class":"ember-view occludable-update"})
        conn_names = Counter()
        p_text,urls =[],[]
        for container in containers:

            try:
                ## get poster's name
                name_box = container.find("div",{"class":"update-components-actor"})
                name = name_box.find("a")['href'].split("?")[0]
                #name  = name.text.strip()
                conn_names.update([name]) 
                text_box = container.find("div",{"class":"feed-shared-update-v2__description-wrapper"})
                text = text_box.find("span",{"dir":"ltr"})
                post_text = text.text.strip()
                p_text.append(post_text)
                #print(post_text)
                if "https" in post_text:
                    post_url = re.findall("(?P<url>https?://[^\s]+)", post_text)
                else:
                    post_url = ""
                #print(post_url)
                urls.append(post_url)
            except:
                #print(text_box)
                pass
            
        # Extract shared URLs from post data
        # ...
        
        # Create Post objects and return them
        # ...
    
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

