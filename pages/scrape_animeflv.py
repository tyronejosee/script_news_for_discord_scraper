"""
Scraper for AnimeFLV.
"""

from typing import List, Any

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet


def scrape_animeflv() -> List[str]:
    """Scraper for AnimeFLV."""
    url: str = "https://m.animeflv.net"
    response: requests.Response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <li> elements with class "Episode"
    divs: ResultSet[Any] = soup.find_all("li", class_="Episode")
    links: List[str] = []

    for div in divs:
        # Find the <a> tag and extract the href (link)
        a_tag = div.find("a", href=True)
        if a_tag:
            link: str = a_tag["href"]
            if not link.startswith("http"):
                link = f"{url}{link}"

            # Find the <figure> tag with class "Image"
            figure = div.find("figure", class_="Image")
            img_link = None
            if figure:
                img_tag = figure.find("img")
                if img_tag and img_tag.get("src"):
                    img_link = img_tag["src"]
                    if not img_link.startswith("http"):
                        img_link = f"{url}{img_link}"

            # Find the <h2> tag with class "Title"
            title = div.find("h2", class_="Title")
            title_text = title.get_text(strip=True) if title else "No title"

            # Find the <p> tag for the episode description
            p_tag = div.find("p")
            episode = p_tag.get_text(strip=True) if p_tag else ""

            episode_number: str = (
                episode.replace("Episodio", "").strip()
                if episode.startswith("Episodio")
                else "Unknown"
            )
            formatted_episode: str = f"Episodio {episode_number}"

            links.append(
                f"# {title_text} - {formatted_episode}\n\nImage: {img_link}\nLink: <{link}>"
            )

    return links
