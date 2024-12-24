"""
Scraper for SomosKudazai.
"""

import requests
from bs4 import BeautifulSoup


def scrape_somoskudazai():
    url = "https://somoskudasai.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    selectors = soup.find_all("a", class_="lnk-blk")
    links = []
    for div in selectors:
        links.append(div["href"])
    return links
