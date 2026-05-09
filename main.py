'''
main.py
----------
Entry point for Gap Radar.

Orchestrates the full pipeline:
1. Fetches and formats post titles and help center articles
2. Sends both datasets to Gemini for gap analysis
3. Generate a styled HTML report with the results
'''

from gap_analyzer import setup_client, get_content, analyze
from report_generator import generate_report

if __name__ == "__main__":
    client = setup_client()
    prompt = get_content()
    analysis = analyze(client, prompt)
    generate_report(analysis)
