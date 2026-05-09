# Gap Radar

A Python automation pipeline that identifies training gaps in a product's help center by cross-referencing real user community questions against existing documentation — powered by Google Gemini. This is part of a personal bootcamp portfolio projects.

## Features
- HTML parser extracting post titles from locally saved community forum pages
- Help center scraper collecting article titles across all documentation categories (respecting `/robots.txt` and public access only)
- AI-powered gap analysis via Google Gemini — no keyword matching
- Strict prompt formatting to ensure consistent, parser-friendly output
- Retry logic for transient API failures (3 attempts, 3 seconds apart)
- Styled HTML report with gap cards, stats bar, and branding — ready to screenshot

## Requirements
- Python 3.12+
- Google Gemini API key (free tier)

## Installation
```
pip install -r requirements.txt
```

## Setup
1. Clone the repo
2. Add your API key to a `.env` file:
```
GEMINI_API_KEY=your_key_here
```
3. Save community forum page(s) locally as HTML files and add their paths to `HTML_FILE_PATHS` in `config.py`
4. Adjust extraction logic to match your locally saved HTML file

## How to Run
```
python main.py
```
The report is generated at `gap_report.html`.

## Pipeline

| Step | Script | Input | Output |
|------|--------|-------|--------|
| 1 | `community_scraper.py` | Local HTML files | Formatted post titles string |
| 2 | `helpcenter_scraper.py` | Help center category URLs | Formatted article titles string |
| 3 | `gap_analyzer.py` | Post titles + article titles | Plain-text gap analysis |
| 4 | `report_generator.py` | Gap analysis text | `gap_report.html` |

## AI Gap Analysis

Both datasets are embedded into a structured prompt and sent to Gemini. The model cross-references community questions against existing help articles and returns a ranked list of 10 training gaps — each with a topic, explanation, and supporting questions sourced directly from the community data.

A strict output format is enforced in the prompt to ensure the response is consistently parseable regardless of model variation between runs.

## Project Structure
```
gap-radar/
├── main.py                 # Entry point — orchestrates the full pipeline
├── community_scraper.py    # Parses locally saved HTML files for post titles
├── helpcenter_scraper.py   # Scrapes help center article titles by category
├── gap_analyzer.py         # Builds the prompt and calls the Gemini API
├── report_generator.py     # Parses Gemini's response and renders the HTML report
├── config.py               # Central config — file paths, URLs, model, output name
├── requirements.txt
├── .env.example            # Environment variable template
├── .gitignore
└── README.md
```

## Environment Variables
```
GEMINI_API_KEY=your_key_here
```

## Limitations
- Community data is sourced from manually saved forum pages — titles were collected by browsing public posts and saving the page(s) locally for offline parsing
- Help center scraper targets a specific article card CSS class — may break if the site's HTML structure changes
- Gemini free tier: ~15 RPM, ~1000 RPD on `gemini-2.5-flash-lite`
- Gap analysis quality depends on the volume and relevance of community posts provided

## Author
Ghaleb Khadra