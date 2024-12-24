"""
Scraper for Google Trends.
"""

import requests
from bs4 import BeautifulSoup


def scrape_google_trends():
    url = "https://trends.google.com/trending?geo=CL"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    selectors = soup.find_all("div", class_="mZ3RIc")
    links = []
    for selector in selectors:
        links.append(selector)
    return links
