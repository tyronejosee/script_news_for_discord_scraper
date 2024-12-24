"""
Scraper for Google Trends.
"""

from typing import List, Any

from pytrends.request import TrendReq


def scrape_google_trends() -> List[str]:
    pytrends: TrendReq = TrendReq(hl="en-US", tz=360)
    links: List[str] = []

    trending_searches: Any = pytrends.trending_searches(pn="chile")
    trends: List[str] = trending_searches[0].tolist()

    for trend in trends:
        links.append(f"🔍 **{trend}**")
    return links
