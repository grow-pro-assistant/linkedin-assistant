import json
from scraper.scraper import Scraper
from scraper import utils

## Define the URL of the profile to scrape
profile_url, driver = utils.access_profile()

## Create a Scraper object with the profile URL
scraper = Scraper(profile_url)


## Scrape the profile data
#profile = scraper.scrape_profile()

## Scrape the posts
data, conn_names, driver = scraper.scrape_posts(driver)

## 
print('profile_url;', profile_url)
del conn_names[profile_url.strip('/')]
scraper.scrape_conn_posts(driver,conn_names, data)


""""
# Iterate over the posts and crawl each shared URL
for post in posts:
    for url in post.shared_urls:
        crawled_data = crawl_url(url)
        # Do something with the crawled data, such as writing it to a JSON file
 """