import json
from scraper.scraper import Scraper

# Define the URL of the profile to scrape
profile_url = "https://www.example.com/profile"

# Create a Scraper object with the profile URL
scraper = Scraper(profile_url)

# Scrape the profile data
profile = scraper.scrape_profile()

# Scrape the posts
posts = scraper.scrape_posts()

# Define a dictionary to store the scraped data
data = {
    "profile": profile.__dict__,
    "posts": [post.__dict__ for post in posts]
}

# Write the scraped data to a JSON file
with open("scraped_data.json", "w") as f:
    json.dump(data, f)

# Iterate over the posts and crawl each shared URL
for post in posts:
    for url in post.shared_urls:
        crawled_data = crawl_url(url)
        # Do something with the crawled data, such as writing it to a JSON file
