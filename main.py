"""
News for Discord Scraper
"""

import json
import os
import logging

import requests
from dotenv import load_dotenv
from .logging_configs import setup_logging

load_dotenv()
setup_logging()

WEBHOOK_URL: str = os.environ.get("WEBHOOK_URL")
if WEBHOOK_URL is None:
    raise ValueError("WEBHOOK_URL environment variable is not set.")

DATA_FILE = "./data/scraped_data.json"
if DATA_FILE is None:
    raise ValueError("DATA_FILE environment variable is not set.")


def load_persisted_data():
    """Loads the persisted data from the file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []


def save_data(new_data):
    """Saves the new data to the file."""
    with open(DATA_FILE, "w") as file:
        json.dump(new_data, file)


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
    else:
        logging.error(f"Error sending message: {response.status_code}")


def scrape_and_send():
    # Load the already persisted data
    existing_data = load_persisted_data()

    # Simulating new scraped data
    scraped_data = ["News 1", "News 2"]

    # Filter new data that is not in the persisted list
    new_data = [item for item in scraped_data if item not in existing_data]

    if new_data:
        # Send to Discord
        for item in new_data:
            send_to_discord(item)

        # Save the new persisted data
        save_data(existing_data + new_data)
    else:
        logging.error("No new data to send.")


if __name__ == "__main__":
    scrape_and_send()
