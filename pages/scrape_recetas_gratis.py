"""
Scraper for Recetas Gratis.
"""

import requests
from bs4 import BeautifulSoup


def scrape_recetas_gratis():
    url = "https://www.recetasgratis.net"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    selectors = soup.find_all("a", class_="titulo titulo--bloque")
    links = []
    for div in selectors:
        links.append(div["href"])
    return links
