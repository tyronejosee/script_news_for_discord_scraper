"""
Scraper for La Cuarta.
"""

import requests
from bs4 import BeautifulSoup


def scrape_lacuarta():
    """Scraper for La Cuarta."""
    url = "https://www.lacuarta.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    divs = soup.find_all("div", class_="story-card-image article-image")
    links = []
    for div in divs:
        a_tag = div.find("a", href=True)
        if a_tag:
            link = a_tag["href"]
            if not link.startswith("http"):
                link = f"https://www.lacuarta.com{link}"
            links.append(link)

    return links
