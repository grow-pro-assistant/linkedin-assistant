import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    # Fetch the page HTML using the requests library
    response = requests.get(url)
    html = response.content

    # Return the page HTML
    return html

def parse_links(html, base_url):
    # Parse the page HTML to extract the links
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            # Make the link absolute using the base URL
            abs_url = make_absolute_url(href, base_url)
            links.append(abs_url)

    # Return the links
    return links

def make_absolute_url(url, base_url):
    # Make a URL absolute using the base URL
    if url.startswith("http"):
        return url
    else:
        return base_url + url
