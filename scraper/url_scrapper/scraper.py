from model import Page

class Scraper:
    def __init__(self, url):
        self.url = url
    
    def scrape(self):

        # Parse the page HTML and create a Page object
        page = Page(self.url)
        page.parse()

        # Return the Page object
        return page
