"""
community_scraper.pu
-------------------------
Parses locally saved HTML files from a public software community forum to extract post titles for use in gap analysis.

Why local files?
    The forum's policy disallowed bot scraping. Saving pages locally and parsing them offline is a clean, dependency-
    free alternative for proof of concept and learning purposes.

Usage:
    Pass a list of file paths to get_post_titles().
    Multiple files are supported — duplicates are removed automatically.
"""

from bs4 import BeautifulSoup


def get_post_titles(file_paths):
    """
    Extract and deduplicate post titles from one or more saved HTML files.

    Each file is parsed with BeautifulSoup to locate community post elements and extract their title attributes. Titles
    are collected into a set to eliminate duplicates across files.

    Args:
        file_paths (list[str]): Paths to locally saved HTML files.

    Returns:
        str: A numbered, newline-separated string of post titles.
            Example:
                1. How do I use formulas in a database?
                2. Product is so slow on mobile
    """
    post_titles = set()

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            contents = f.read()

        soup = BeautifulSoup(contents, "html.parser")
        raw_posts = soup.find_all("shreddit-post")

        for post in raw_posts:
            post_titles.add(post.get("post-title"))

    titles_list = [f"{i + 1}. {title}" for i, title in enumerate(post_titles)]
    return "\n".join(titles_list)
