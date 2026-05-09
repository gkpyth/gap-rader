"""
report_generator.py
--------------------
Parses Gemini's plain-text gap analysis and renders it as a styled HTML report saved to disk.

Pipeline:
    1. parse_gaps()         - extracts structured data from Gemini's response
    2. build_gap_cards()    - converts structured data into HTML card elements
    3. generate_report()    - assembles the full HTML page and writes it to file
"""

import re
from config import REPORT_OUTPUT


def parse_gaps(text):
    """
    Parse Gemini's plain-text response into a list of structured gap dictionaries.

    Splits the response on 'GAP #N:' markers and extracts the title, explanation, and supporting questions for each
    gap using regex.

    Args:
        text (str): Raw plain-text response from Gemini.

    Returns:
        list[dict]: List of gap dictionaries, each containing:
            - number              (str): Gap number e.g. "1"
            - title               (str): Gap topic title
            - why                 (str): Explanation of why it's a gap
            - questions     (list[str]): 3 supporting community questions
    """
    gaps = []
    sections = re.split(r'GAP #(\d+):\s*', text)

    i = 1
    while i < len(sections) - 1:
        number = sections[i]
        content = sections[i + 1]

        title_line = content.split('\n')[0]
        title = title_line.strip()

        why_match = re.search(r"Why it's a gap:\s*(.+?)(?=Supporting questions:|$)", content, re.DOTALL)
        why = why_match.group(1).strip() if why_match else ""

        questions_match = re.search(r"Supporting questions:\s*(.+?)$", content, re.DOTALL)
        questions_raw = questions_match.group(1).strip() if questions_match else ""
        questions = re.findall(r'-\s+"?([^"\n]+)"?', questions_raw)
        questions = [q.strip().strip('"') for q in questions if q.strip()][:4]

        gaps.append({'number': number, 'title': title, 'why': why, 'questions': questions})
        i += 2

    return gaps

def build_gap_cards(gaps):
    """
    Convert a list of gap dictionaries into HTML card elements.

    Each gap becomes a self-contained card with a header, explanation, and a list of supporting community questions.

    Args:
         gaps (list[dict]): Structured gap data from parse_gaps().

    Returns:
        str: HTML string containing all gap cards ready for insertion.
    """
    cards_html = ""
    for gap in gaps:
        questions_html = "".join(f'<li>"{q}"</li>' for q in gap['questions'])
        cards_html += f"""
        <div class="gap-card">
            <div class="gap-header">
                <span class="gap-number">GAP #{gap['number']}</span>
                <h2 class="gap-title">{gap['title']}</h2>
            </div>
            <div class="gap-body">
                <div class="gap-section">
                    <div class="gap-section-label">Why it's a gap</div>
                    <p class="gap-section-text">{gap['why']}</p>
                </div>
                <div class="gap-section">
                    <div class="gap-section-label">Supporting questions from the community</div>
                    <ul class="gap-questions">{questions_html}</ul>
                </div>
            </div>
        </div>
        """
    return cards_html

def generate_report(analysis):
    """
    Orchestrate parsing, card building, and HTML report generation.

    Calls parse_gaps() and build_gap_cards() to convert the raw analysis into HTML, then assembles the full page with
    header, stats bar, and footer, before writing it to the output file defined in config.py.

    Args:
         analysis (str): Raw plain-text gap analysis from Gemini.
    """
    gaps = parse_gaps(analysis)
    cards_html = build_gap_cards(gaps)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gap Radar - Training Gap Analysis</title>
        <link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet">
        <style>
            *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
     
            :root {{
                --bg:           #0c0c0e;
                --surface:      #141416;
                --border:       #222226;
                --accent:       #f0a44a;
                --accent-dim:   rgba(240, 164, 74, 0.10);
                --text:         #e8e8ec;
                --text-dim:     #9999a8;
                --text-muted:   #55555f;
            }}
     
            body {{
                background: var(--bg);
                color: var(--text);
                font-family: 'DM Sans', sans-serif;
                font-weight: 300;
                line-height: 1.7;
                min-height: 100vh;
            }}
     
            /* ── Header ─────────────────────────────────── */
            .report-header {{
                border-bottom: 1px solid var(--border);
                padding: 3rem 4rem;
                display: flex;
                align-items: flex-end;
                justify-content: space-between;
                gap: 2rem;
            }}
     
            .brand {{
                font-family: 'Syne', sans-serif;
                font-weight: 700;
                font-size: 0.7rem;
                letter-spacing: 0.22em;
                text-transform: uppercase;
                color: var(--accent);
                margin-bottom: 0.75rem;
            }}
     
            .report-title {{
                font-family: 'Syne', sans-serif;
                font-weight: 700;
                font-size: 2.4rem;
                line-height: 1.1;
            }}
     
            .report-subtitle {{
                margin-top: 0.4rem;
                color: var(--text-dim);
                font-size: 0.9rem;
            }}
     
            .header-meta {{
                text-align: right;
                color: var(--text-muted);
                font-size: 0.78rem;
                line-height: 2;
            }}
     
            .header-meta strong {{
                color: var(--text-dim);
                font-weight: 400;
                display: block;
                line-height: 1.2;
            }}
     
            /* ── Stats bar ───────────────────────────────── */
            .stats-bar {{
                display: flex;
                border-bottom: 1px solid var(--border);
            }}
     
            .stat {{
                flex: 1;
                padding: 1.5rem 4rem;
                border-right: 1px solid var(--border);
            }}
     
            .stat:last-child {{ border-right: none; }}
     
            .stat-value {{
                font-family: 'Syne', sans-serif;
                font-weight: 700;
                font-size: 2.2rem;
                color: var(--accent);
                line-height: 1;
            }}
     
            .stat-label {{
                font-size: 0.72rem;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.1em;
                margin-top: 0.4rem;
            }}
     
            /* ── Body ────────────────────────────────────── */
            .report-body {{
                max-width: 920px;
                margin: 0 auto;
                padding: 4rem;
            }}
     
            .section-heading {{
                font-size: 0.68rem;
                font-weight: 500;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                color: var(--text-muted);
                margin-bottom: 2.5rem;
                display: flex;
                align-items: center;
                gap: 1rem;
            }}
     
            .section-heading::after {{
                content: '';
                flex: 1;
                height: 1px;
                background: var(--border);
            }}
     
            /* ── Gap cards ───────────────────────────────── */
            .gap-card {{
                margin-bottom: 1.5rem;
                border: 1px solid var(--border);
                border-radius: 8px;
                overflow: hidden;
                transition: border-color 0.2s ease;
            }}
     
            .gap-card:hover {{
                border-color: rgba(240, 164, 74, 0.35);
            }}
     
            .gap-header {{
                background: var(--surface);
                padding: 1.25rem 1.75rem;
                display: flex;
                align-items: center;
                gap: 1rem;
                border-bottom: 1px solid var(--border);
            }}
     
            .gap-number {{
                font-family: 'Syne', sans-serif;
                font-weight: 700;
                font-size: 0.8rem;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                color: var(--accent);
                background: var(--accent-dim);
                padding: 0.3rem 0.65rem;
                border-radius: 4px;
                white-space: nowrap;
                flex-shrink: 0;
            }}
     
            .gap-title {{
                font-family: 'Syne', sans-serif;
                font-weight: 700;
                font-size: 1rem;
                color: var(--text);
                line-height: 1.3;
            }}
     
            .gap-body {{
                padding: 1.5rem 1.75rem;
                display: flex;
                flex-direction: column;
                gap: 1.25rem;
            }}
     
            .gap-section-label {{
                font-size: 0.68rem;
                font-weight: 500;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: var(--text-muted);
                margin-bottom: 0.5rem;
            }}
     
            .gap-section-text {{
                color: var(--text-dim);
                font-size: 0.88rem;
                line-height: 1.75;
            }}
     
            .gap-questions {{
                list-style: none;
                display: flex;
                flex-direction: column;
                gap: 0.4rem;
            }}
     
            .gap-questions li {{
                color: var(--text-dim);
                font-size: 0.85rem;
                font-style: italic;
                padding: 0.55rem 1rem;
                background: rgba(255, 255, 255, 0.025);
                border-left: 2px solid var(--accent);
                border-radius: 0 4px 4px 0;
            }}
     
            /* ── Footer ──────────────────────────────────── */
            .report-footer {{
                border-top: 1px solid var(--border);
                padding: 1.75rem 4rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                color: var(--text-muted);
                font-size: 0.78rem;
            }}
     
            .footer-brand {{
                font-family: 'Syne', sans-serif;
                font-weight: 700;
                color: var(--accent);
                letter-spacing: 0.12em;
            }}
        </style>
    </head>
    <body>
        <header class="report-header">
            <div>
                <div class="brand">Gap Radar</div>
                <h1 class="report-title">Training Gap Analysis</h1>
                <p class="report-subtitle">Notion Help Center vs. Community Questions</p>
            </div>
            <div class="header-meta">
                <strong>Data Source</strong>r/Notion · Top Posts (Monthly)
                <strong>Reference</strong>notion.com/help · All Categories
                <strong>Model</strong>Gemini 2.5 Flash Lite
            </div>
        </header>
        
        <div class="stats-bar">
            <div class="stat">
                <div class="stat-value">100</div>
                <div class="stat-label">Community Posts Analyzed</div>
            </div>
            <div class="stat">
                <div class="stat-value">248</div>
                <div class="stat-label">Help Articles Scanned</div>
            </div>
            <div class="stat">
                <div class="stat-value">10</div>
                <div class="stat-label">Training Gaps Identified</div>
            </div>
        </div>
        
        <main class="report-body">
            <div class="section-heading">Identified Gaps</div>
            {cards_html}
        </main>
        
        <footer class="report-footer">
            <div>Build with Python · BeautifulSoup · Gemini API by <span>Ghaleb Khadra</span></div>
            <div class="footer-brand">GAP RADAR</div>
        </footer>
    </body>
    </html>
    """

    with open(REPORT_OUTPUT, "w", encoding="utf-8") as file:
        file.write(html_content)
