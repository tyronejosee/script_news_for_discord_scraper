"""
Scraper for Recetas Gratis.
"""

from typing import List, Any

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet

from core.utils import format_title


def scrape_recetas_gratis() -> List[str]:
    url = "https://www.recetasgratis.net"
    response: requests.Response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    selectors: ResultSet[Any] = soup.find_all(
        "a",
        class_="titulo titulo--bloque",
    )
    links: List[str] = []
    for selector in selectors:
        name: str = selector.get_text(strip=True)
        url: str = selector["href"]
        cleaned_name: str = format_title(
            name.replace("Receta de ", "") if "Receta de " in name else name
        )
        links.append(f"# {cleaned_name}\n\nLink: {url}")
    return links
