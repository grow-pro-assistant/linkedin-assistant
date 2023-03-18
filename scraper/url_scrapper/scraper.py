from model import Page
from utils import fetch_page
import requests
from bs4 import BeautifulSoup
import pandas as pd
class Scraper:
    def __init__(self, url):
        self.url = url
    
    def scrape(self):
        # Fetch the page HTML
        html = fetch_page(self.url)

        # Parse the page HTML and create a Page object
        page = Page(self.url)
        page.parse(html)

        # Return the Page object
        return page
