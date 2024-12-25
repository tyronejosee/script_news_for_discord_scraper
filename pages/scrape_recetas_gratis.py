"""
Scraper for Recetas Gratis.
"""

import logging
from typing import List, Any

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet

from core.logging import setup_logging
from core.utils import format_title

setup_logging()


def scrape_recetas_gratis() -> List[str]:
    url = "https://www.recetasgratis.net/"
    headers: dict[str, str] = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    response: requests.Response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    if response.status_code == 403:
        logging.error(f"Access forbidden: {response.text}")

    selectors: ResultSet[Any] = soup.find_all(
        "a",
        class_="titulo titulo--bloque",
    )
    logging.info(selectors)

    links: List[str] = []
    for selector in selectors:
        name: str = selector.get_text(strip=True)
        url: str = selector["href"]
        cleaned_name: str = format_title(
            name.replace("Receta de ", "") if "Receta de " in name else name
        )
        links.append(f"# {cleaned_name}\n\nLink: {url}")
    return links
