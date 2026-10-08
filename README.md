# web-puller

Playwright WebKit browser automation script. Logs into sites, pulls data
from target pages, saves to JSON.

Built by Alttawan Hensley (Alt Tate).

## What it does

- Opens a URL in a headless WebKit browser
- Optionally logs in (username/password)
- Extracts: page title, meta description, headings, links, body text
- Saves everything to a timestamped JSON file

## Install

Requires Python 3.8+ on a glibc system (Ubuntu, Debian, macOS, Windows).
Does NOT work on Alpine Linux (musl) - use Ubuntu or a-Shell on iOS.

    pip install -r requirements.txt
    playwright install webkit

## Usage

    python web_ingest.py --url https://example.com --out data.json

With login:

    python web_ingest.py --url https://example.com --username me@x.com --password secret --out data.json

## Output format

    {
      "url": "...",
      "title": "...",
      "meta_description": "...",
      "headings": ["..."],
      "links": ["..."],
      "body_text": "...",
      "extracted_at": "..."
    }

## Pricing

- Single script: $500
- Custom build (multi-step, scheduling, error handling): $750-$1,500
- Monthly retainer (ongoing automation): $300/mo

## Contact

Open an issue on this repo, or message @Tawns-lab on X.
