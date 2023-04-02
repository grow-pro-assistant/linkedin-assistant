import requests
from bs4 import BeautifulSoup
import json
from .utils import parse_links


class Page:
    def __init__(self, url):
        self.json_dict = None
        self.text = ''
        self.heading = None
        self.url = url
        self.links = []
        self.metadata = ''
        self.headings = []
        # self.url = url
        # self.description = None
        # self.keywords = []
    
    def parse_json(self):
        first_heading = True

        for d in self.json_dict:
            if d.get("text") == "Metadata":
                for c in d.get('content', []):
                    self.metadata += c.get("text") + '\n' 
            elif d.get("tag_name").startswith("h"):
                if first_heading:
                    self.heading = d.get("text")
                    first_heading = False
    
                self.headings.append(d.get("text"))
                self.text += d.get("text") + "\n"
            for c in d.get("content", []):
                if c.get("tag_name").startswith("h"):
                    self.headings.append(c.get("text"))
                    self.text += c.get("text") + "\n"
                elif c.get("tag_name") == "ul":
                    self.text += c.get("text").replace("\n", "") + "\n"
                    for item in c.get("list_items", []):
                        self.text += item + "\n"
                elif c.get("tag_name") == "p":
                    self.text += c.get("text") + "\n"

    def parse(self, ignore_header_footer = False):
        # send request to the given URL
        response = requests.get(self.url)
        
        # parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # find the main content area of the webpage (ignoring header and footer)
        main_content = soup.find('body')
        if ignore_header_footer:
            header = main_content.find('header')
            footer = main_content.find('footer')
            if header:
                header.extract()
            if footer:
                footer.extract()
        
        # find the main content section of the article
        article = main_content.find('article')
        
        # create an empty array to store JSON objects
        data = []
        
        # create a dummy header object for text before the first header tag
        dummy_header = {'tag_name': 'h0', 'text': 'Metadata', 'content': []}
        
        # flag to keep track of whether we have encountered the first header tag
        found_first_header = False
        
        # add all text and list elements before the first header tag to the dummy header object
        for tag in article.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ol', 'ul']):
            text = tag.text.strip().replace(u'\xa0', u' ').replace('\n\n', ' ').replace('"', '\\"').replace(u'\u2026', '...').replace(u'\u2019', "'").replace(u'\u201c', '"').replace(u'\u201d', '"')
            if not found_first_header:
                # check if the current tag is a header tag
                if tag.name.startswith('h'):
                    found_first_header = True
                    data.append({'tag_name': tag.name, 'text': text, 'content': []})
                # if we haven't encountered the first header tag yet,
                # add the element to the dummy header object
                else:
                    dummy_header['content'].append({'tag_name': tag.name, 'text': text})  
            else:
                # create a JSON object for each element
                obj = {'tag_name': tag.name, 'text': text}
                
                # if the element is an ordered list or unordered list,
                # extract the list items and add them to the JSON object
                if tag.name == 'ol' or tag.name == 'ul':
                    items = []
                    for li in tag.find_all('li'):
                        items.append(li.text.strip())
                    obj['list_items'] = items
                
                # add the JSON object to the array
                if tag.name.startswith('h'):
                    # create a new object for each heading and add it to the array
                    data.append({'tag_name': tag.name, 'text': text, 'content': []})
                else:
                    # add the object to the last heading object in the array
                    data[-1]['content'].append(obj)
    
        
        # add the dummy header object to the array if there is content
        if dummy_header['content']:
            data = [dummy_header] + data
    

        # assign the array of JSON objects
        self.json_dict = data

        self.parse_json()

        self.links = parse_links(response.text, self.url)