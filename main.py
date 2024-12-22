"""
News for Discord Scraper
"""

import json
import os
import logging
import time
import requests

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from supabase import create_client, Client

from logging_configs import setup_logging

load_dotenv()
setup_logging()


WEBHOOK_URL: str = os.environ.get("WEBHOOK_URL")
if WEBHOOK_URL is None:
    raise ValueError("WEBHOOK_URL environment variable is not set.")

# Supabase credentials
SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")
if SUPABASE_URL is None or SUPABASE_KEY is None:
    raise ValueError("Supabase credentials not set in environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def load_persisted_data():
    """Loads the persisted data from Supabase."""
    try:
        response = supabase.table("scraped_data").select("*").execute()
        return [record["url"] for record in response.data]
    except Exception as e:
        logging.error(f"Error loading data from Supabase: {e}")
        return []


def save_data(new_data):
    """Saves the new data to Supabase."""
    try:
        for item in new_data:
            # Check if URL already exists in Supabase to avoid duplicates
            existing = (
                supabase.table("scraped_data").select("url").eq("url", item).execute()
            )
            if existing.data:
                logging.info(f"Duplicate URL found, skipping: {item}")
                continue
            # Insert new data
            supabase.table("scraped_data").insert({"url": item}).execute()
        logging.info("New data saved successfully.")
    except Exception as e:
        logging.error(f"Error saving data to Supabase: {e}")


def send_to_discord(message):
    """Sends a message to Discord via the webhook."""
    payload = {"content": message}  # The content of the message
    headers = {"Content-Type": "application/json"}

    # Make the POST request to the webhook
    response = requests.post(
        WEBHOOK_URL,
        data=json.dumps(payload),
        headers=headers,
    )

    # Check if the request was successful
    if response.status_code == 204:
        logging.info(f"Message successfully sent: {message}")
    elif response.status_code == 429:
        logging.error("Rate limit reached.")
    else:
        logging.error(f"Error sending message: {response.status_code}")


def scrape_lacuarta():
    url = "https://www.lacuarta.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    divs = soup.find_all("div", class_="story-card-image article-image")

    links = []
    for div in divs:
        a_tag = div.find("a", href=True)
        if a_tag:
            link = a_tag["href"]
            if not link.startswith("http"):
                link = f"https://www.lacuarta.com{link}"
            links.append(link)

    return links


def scrape_and_send():
    # Load the already persisted data
    existing_data = set(load_persisted_data())
    scraped_data = set(scrape_lacuarta())
    new_data = scraped_data - existing_data

    if new_data:
        # Send to Discord
        for item in new_data:
            send_to_discord(item)
            time.sleep(1)

        # Save the new persisted data
        save_data(new_data)
    else:
        logging.error("No new data to send.")


if __name__ == "__main__":
    scrape_and_send()
