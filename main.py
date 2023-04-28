import json
from scraper.scraper import Scraper
from scraper import utils

## Define the URL of the profile to scrape
profile_url,driver = utils.get_profile()

## Create a Scraper object with the profile URL
scraper = Scraper(profile_url)


## Scrape the profile data
#profile = scraper.scrape_profile()

## Scrape the posts
ids,posts,actors,urls,conn_names,driver, url_texts = scraper.scrape_posts(driver)

#print(ids)
#utils.write_json(ids,posts,actors,urls, url_texts)
## 
del conn_names[profile_url]
scraper.scrape_conn_posts(driver,conn_names)


""""
# Iterate over the posts and crawl each shared URL
for post in posts:
    for url in post.shared_urls:
        crawled_data = crawl_url(url)
        # Do something with the crawled data, such as writing it to a JSON file
 """