"""
Scraper for La Cuarta.
"""

from typing import List, Any

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet


def scrape_lacuarta() -> List[str]:
    url = "https://www.lacuarta.com/"
    response: requests.Response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    divs: ResultSet[Any] = soup.find_all(
        "div",
        class_="story-card-image article-image",
    )
    links: List[str] = []
    for div in divs:
        a_tag = div.find("a", href=True)
        if a_tag:
            link: str = a_tag["href"]
            if not link.startswith("http"):
                link: str = f"https://www.lacuarta.com{link}"
            links.append(link)

    return links
