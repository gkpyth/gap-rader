"""
gap_analyzer.py
--------------------
Handles communication with the Gemini API to perform training gap analysis.

Takes community post titles and help center article titles as inputs, constructs a structured prompt, and sends it to
Gemini for analysis.
Returns a plain-text gap report in a strict, parser-friendly format.

Requires:
    GEMINI_API_KEY in .env
"""

import os
import time
from config import GEMINI_MODEL, HTML_FILE_PATHS, HELPCENTER_CATEGORIES
from google import genai
from community_scraper import get_post_titles
from helpcenter_scraper import get_help_articles
from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def construct_prompt():
    """
    Collect data from both sources and build the Gemini prompt.

    Calls get_post_titles() and get_help_articles() to fetch the two datasets, then embeds them into a structured
    prompt that instructs Gemini to identify and rank training gaps.

    Returns:
        str: The fully constructed prompt ready to send to Gemini.
    """
    post_titles = get_post_titles(HTML_FILE_PATHS)
    help_articles = get_help_articles(HELPCENTER_CATEGORIES)

    prompt = f"""
    You are an expert in customer education and product enablement.

    Below are two datasets:

    1. COMMUNITY QUESTIONS: Real questions and struggles posted by software users on a public forum.
    2. HELP CENTER ARTICLES: Titles of all existing articles in the product's official help center.

    Your job is to identify TRAINING GAPS — topics that users frequently struggle with or ask about, but that are either missing or insufficiently covered in the help center.

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

    IMPORTANT: Follow the output format below EXACTLY. No markdown, no bold, no headers, no bullet symbols other than a dash. Do not deviate.
    
    Output format:
    GAP #1: [Topic title]
    Why it's a gap: [Explanation]
    Supporting questions:
    - "[Question from community]"
    - "[Question from community]"
    - "[Question from community]"

    GAP #2: [Topic title]
    Why it's a gap: [Explanation]
    Supporting questions:
    - "[Question from community]"
    - "[Question from community]"
    - "[Question from community]"
    
    ...continue this exact pattern for all 10 gaps.
    """

    return prompt

def setup_client():
    """
    Initialize and return an authenticated Gemini API client.

    Reads the API key from the environment. Raises a clear error if the key is missing.

    Returns:
        genai.Client: Authenticated Gemini client ready to use.

    Raises:
        EnvironmentError: If GEMINI_API_KEY is not set in the environment.
    """
    if not GEMINI_API_KEY:
        raise EnvironmentError(
            "GEMINI_API_KEY not found. Add it to your .env file."
        )
    return genai.Client(api_key=GEMINI_API_KEY)

def analyze(client, prompt):
    """
    Send the prompt to Gemini and return the gap analysis as plain text.

    Retries up to 3 times on failure with a short delay between attempts.
    Raises an error if Gemini returns an empty response or all retries fail.

    Args:
         client (genai.Client): Authenticated Gemini client.
         prompt (str): The fully constructed analysis prompt.

    Returns:
        str: Plain-text gap analysis in the structured format defined in the prompt.

    Raises:
        ValueError: If Gemini returns an empty or invalid response.
        Exception: Re-raises the last exception if all retries are exhausted.
    """
    MAX_RETRIES = 3
    RETRY_DELAY = 3
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            result = response.text

            if not result or not result.strip():
                raise ValueError("Gemini returned an empty or invalid response")

            return result

        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                print(f"attempt {attempt} failed ({e}) - retrying in {RETRY_DELAY} sec...")
                time.sleep(RETRY_DELAY)

    raise last_error