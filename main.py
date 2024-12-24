"""
News for Discord Scraper
"""

import json
import logging
import time
import argparse

import requests
from dotenv import load_dotenv

from core.config import WEBHOOKS
from core.logging import setup_logging
from core.db import load_data
from core.utils import save_results
from pages.scrape_lacuarta import scrape_lacuarta
from pages.scrape_somoskudasai import scrape_somoskudazai
from pages.scrape_animeflv import scrape_animeflv
from pages.scrape_recetas_gratis import scrape_recetas_gratis

# from pages.scrape_google_trends import scrape_google_trends

load_dotenv()
setup_logging()


def send_to_discord(message, webhook_url):
    """Sends a message to Discord using the specified webhook."""
    payload = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        webhook_url,
        data=json.dumps(payload),
        headers=headers,
    )

    if response.status_code == 204:
        logging.info(f"Message successfully sent: {message}")
    elif response.status_code == 429:
        logging.error("Rate limit reached.")
    else:
        logging.error(f"Error sending message: {response.status_code}")


def scrape_and_send(scraper_name, scraper_function):
    """Runs a scraper and sends new data to Discord."""
    webhook_url = WEBHOOKS.get(scraper_name)
    if not webhook_url:
        logging.error(f"No webhook configured for {scraper_name}.")
        return

    # Load persisted data
    existing_data = set(load_data())
    scraped_data = set(scraper_function())
    new_data = scraped_data - existing_data

    output_file = "list.txt"
    if new_data:
        # Send to Discord
        for item in new_data:
            send_to_discord(item, webhook_url)
            time.sleep(1)

        # Save new data
        # save_data(new_data)
        save_results(output_file, new_data)
    else:
        logging.info(f"No new data to send from {scraper_name}.")


def scrape_by_interval(interval):
    """Runs scrapers based on the provided interval."""
    if interval == "hourly":
        scrape_and_send("la_cuarta", scrape_lacuarta)
        scrape_and_send("somoskudasai", scrape_somoskudazai)
        scrape_and_send("animeflv", scrape_animeflv)
    elif interval == "daily":
        scrape_and_send("recetas_gratis", scrape_recetas_gratis)
        # scrape_and_send("google_trends", scrape_google_trends)
    else:
        logging.error(f"Invalid interval specified: {interval}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a specific scraper at defined intervals."
    )
    parser.add_argument(
        "interval",
        type=str,
        choices=["hourly", "daily"],
        help="The interval at which to run the scrapers.",
    )
    args = parser.parse_args()

    logging.info(f"Running scraper with interval: {args.interval}")
    scrape_by_interval(args.interval)
