"""
Scraper for CiperChile.
"""

from typing import List, Any

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet


def scrape_ciperchile() -> List[str]:
    url = "https://www.ciperchile.cl/investigacion/"
    response: requests.Response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    selectors: ResultSet[Any] = soup.find_all("a", class_="alticle-link")

    links: List[str] = []
    for div in selectors:
        links.append(div["href"])
    return links
