"""
Scraper for SomosKudazai.
"""

from typing import List, Any

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet


def scrape_somoskudazai() -> List[str]:
    url: str = "https://somoskudasai.com"
    response: requests.Response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    selectors: ResultSet[Any] = soup.find_all("a", class_="lnk-blk")
    links: List[str] = []
    for div in selectors:
        links.append(div["href"])
    return links
