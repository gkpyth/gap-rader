import os
import time
from config import *
from google import genai
from community_scraper import get_post_titles
from helpcenter_scraper import get_help_articles
from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_content():
    post_titles = get_post_titles(HTML_FILE_PATHS)
    help_articles = get_help_articles(HELPCENTER_CATEGORIES)

    prompt = f"""
    You are an expert in customer education and product enablement.

    Below are two datasets:

    1. COMMUNITY QUESTIONS: Real questions and struggles posted by Notion users on Reddit.
    2. HELP CENTER ARTICLES: Titles of all existing articles in Notion's official help center.

    Your job is to identify TRAINING GAPS — topics that Notion users frequently struggle with or ask about, but that are either missing or insufficiently covered in the help center.

    COMMUNITY QUESTIONS:
    {post_titles}

    HELP CENTER ARTICLES:
    {help_articles}

    Instructions:
    - Analyze the community questions and identify recurring topics and themes
    - Cross-reference those themes against the help center articles
    - Identify gaps where user struggles are NOT adequately addressed by existing help content
    - Be specific — don't just say "databases", say what aspect of databases users struggle with
    - Rank the top 10 gaps by how frequently the topic appears in community questions
    - For each gap, provide: the topic, why it's a gap, and 2-3 example questions from the community that support it

    Output format:
    GAP #1: [Topic]
    Why it's a gap: [explanation]
    Supporting questions: [2-3 examples from the community data]

    GAP #2: [Topic]
    ...and so on up to GAP #10.
    """

    return prompt

def setup_client():
    if not GEMINI_API_KEY:
        raise EnvironmentError(
            "GEMINI_API_KEY not found. Add it to your .env file."
        )
    return genai.Client(api_key=GEMINI_API_KEY)

def analyze(client, prompt):
    MAX_RETRIES = 3
    RETRY_DELAY = 3

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            return response.text

        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                print(f"attempt {attempt} failed ({e}) - retrying in {RETRY_DELAY} sec...")
                time.sleep(RETRY_DELAY)

    raise last_error