"""Utility functions for the project."""

import json
import logging

from datetime import datetime

from .config import ROMAN_NUMERALS, EXCEPTIONS
from .logging import setup_logging

setup_logging()


def format_title(title: str) -> str:
    """Formats the text using camel case."""
    words: list[str] = title.split()
    formatted_title: list[str] = [
        (
            word
            if word.upper() in ROMAN_NUMERALS
            else (word.capitalize() if word.lower() not in EXCEPTIONS else word.lower())
        )
        for word in words
    ]
    formatted_title[0] = formatted_title[0].capitalize()
    return " ".join(formatted_title)


def save_results(output_file, new_data):
    """Saves the results to a file."""
    try:
        with open(output_file, "a") as file:
            file.write(json.dumps(list(new_data)) + "\n")
        logging.info(f"Results successfully saved to {output_file}.")
    except Exception as e:
        logging.error(f"Error saving results to file: {e}")


def get_current_timestamp_simple() -> str:
    # Get the current date and time
    now = datetime.now()

    # Format the date as "DD/MM/YYYY"
    return now.strftime("%d/%m/%Y")


def get_current_timestamp_extend() -> str:
    # Define the day and month names in Spanish
    days_of_week: list[str] = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo",
    ]
    months_of_year: list[str] = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]

    # Get the current date and time
    now: datetime = datetime.now()

    # Get the weekday and month, and format the date in Spanish
    weekday: str = days_of_week[now.weekday()]
    day: int = now.day
    month: str = months_of_year[now.month - 1]  # Adjust because month starts from 1
    year: int = now.year

    return f"{weekday}, {day} de {month} {year}"
