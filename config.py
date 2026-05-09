"""
config.py
----------
Central configuration for Gap Radar.

All settings are defined here so nothing is hardcoded elsewhere.
To adapt this tool for a different product, update the file paths, help center URLs, and report output name in this
file only.
"""

# Locally saved HTML files containing community forum posts.
# Add additional file paths here if needed
HTML_FILE_PATHS = [
    "internal/notion.html",
]

# Help center category URLs to scrape article titles from.
# Each URL corresponds to one documentation category.
HELPCENTER_CATEGORIES = [
    "https://www.notion.com/help/category/new-to-notion",
    "https://www.notion.com/help/category/sidebar-navigation",
    "https://www.notion.com/help/category/meet-your-workspace",
    "https://www.notion.com/help/category/account-settings-and-privacy",
    "https://www.notion.com/help/category/write-edit-and-customize",
    "https://www.notion.com/help/category/databases",
    "https://www.notion.com/help/category/database-views",
    "https://www.notion.com/help/category/sharing-and-collaboration",
    "https://www.notion.com/help/category/notion-sites",
    "https://www.notion.com/help/category/import-export-and-integrate",
    "https://www.notion.com/help/category/connections",
    "https://www.notion.com/help/category/automations",
    "https://www.notion.com/help/category/notion-ai",
    "https://www.notion.com/help/category/notion-ai-connectors",
    "https://www.notion.com/help/category/custom-agents",
    "https://www.notion.com/help/category/enterprise-admin",
    "https://www.notion.com/help/category/security-and-privacy",
    "https://www.notion.com/help/category/notion-ai-security",
    "https://www.notion.com/help/category/notion-apps",
    "https://www.notion.com/help/category/notion-mail",
    "https://www.notion.com/help/category/notion-calendar",
    "https://www.notion.com/help/category/template-gallery",
    "https://www.notion.com/help/category/plans-billing-and-payment",
    "https://www.notion.com/help/category/troubleshooting"
]

# Gemini model to use for gap analysis.
# Free tier recommended: gemini-2.5-flash-lite (highest daily limit)
GEMINI_MODEL = "gemini-2.5-flash-lite"

# Output file name for the generated HTML report.
REPORT_OUTPUT = "gap_report.html"