"""
Scraper for LaTercera.
"""

from typing import List

from playwright.sync_api import sync_playwright


def scrape_latercera() -> List[str]:
    url: str = "https://www.latercera.com"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        allowed_prefixes: List[str] = [
            "/pulso/",
            "/mundo/",
            "/nacional/",
            "/tendencias/",
        ]

        selectors = page.locator('a[target="_self"]')

        links: List[str] = []
        for i in range(selectors.count()):
            href = selectors.nth(i).get_attribute("href")
            if href and any(href.startswith(prefix) for prefix in allowed_prefixes):
                links.append(f"{url}{href}")
        return links
