import requests
import time
from bs4 import BeautifulSoup
from config import *


def get_help_articles(url_list):
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
