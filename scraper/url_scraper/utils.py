import requests
from bs4 import BeautifulSoup


def parse_links(html, base_url = None):
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
    elif base_url:
        return base_url + url
    else:
        return url
