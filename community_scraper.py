from bs4 import BeautifulSoup

file_paths = [
    "internal/notion",
]

def get_post_titles(file_paths):
    post_titles = set()

    for file_path in file_paths:
        with open("internal/notion.html", "r", encoding="utf-8") as f:
            contents = f.read()

        soup = BeautifulSoup(contents, "html.parser")
        raw_posts = soup.find_all("shreddit-post")

        for post in raw_posts:
            post_titles.add(post.get("post-title"))

        titles_list = [f"{i + 1}. {title}" for i, title in enumerate(post_titles)]

        return "\n".join(titles_list)
