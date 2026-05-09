"""
helpcenter_scraper.py
-------------------------
Scrapes article titles from a product's public help center documentation.

Iterates through a list of category URLs defined in config.py, fetching each page and extracting article titles using
BeautifulSoup. A short delay between requests is included to avoid hammering the server — always be a polite bot.

The help center is publicly accessible with no login required, and scraping is permitted per the site's robots.txt
"""

import requests
import time
from bs4 import BeautifulSoup


def get_help_articles(url_list):
    """
    Scrape and deduplicate help article titles from a list of category URLs.

    For each URL, fetches the page, parses the HTML, and extracts the title attribute from each article card. Titles
    are collected into a set to eliminate duplicates across categories. A 2-second delay is applied between requests
    to be respectful of the server.

    Args:
        url_list (list[str]): Help center category URLs to scrape.

    Returns:
        str: A numbered, newline-separated string of article titles.
            Example:
                1. Intro to databases
                2. Formula syntax & functions
                3. Sharing & permissions
    """
    help_articles = set()

    for url in url_list:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("article", class_="helpCenterContentPreview_articlePreview__Epc1O")

            for article in articles:
                title = article.find("a")["title"]
                help_articles.add(title)

        else:
            print(f"Failed to retrieve content from '{url}'. Status code: {response.status_code}")

        time.sleep(2)

    articles_list = [f"{i + 1}. {title}" for i, title in enumerate(help_articles)]
    return "\n".join(articles_list)
