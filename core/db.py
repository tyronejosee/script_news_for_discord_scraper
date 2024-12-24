"""Database module for interacting with Supabase."""

import logging
from supabase import create_client, Client

from .config import SUPABASE_URL, SUPABASE_KEY
from .logging import setup_logging

setup_logging()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def load_data():
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
        logging.error(f"Error saving data: {e}")
