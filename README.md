# web-ingest

**Playwright WebKit content ingestion engine.**

Logs into a site, navigates to a target URL, extracts structured data
(title, meta description, headings, links, body text), and saves it as JSON.
Designed as a sellable automation module: swap the config, run it.

Built by Alttawan Hensley (Alt Tate) — https://github.com/Tawns-lab

## What it does

- Opens any URL in a headless **WebKit** browser (Playwright)
- Optionally logs in via a separate login URL (generic form detection)
- Extracts: page title, meta description, headings (h1–h3), links, body text
- Saves everything to a timestamped JSON file
- Cron-ready for scheduled runs

## Install

```bash
pip install -r requirements.txt
playwright install webkit
```

## Usage

```bash
# Basic pull (no login)
python web_ingest.py --url https://example.com --out data.json

# Pull with login
python web_ingest.py --url https://example.com/dashboard \
    --login-url https://example.com/login \
    --username me@example.com --password secret \
    --out data.json

# Scheduled (cron) — daily 9 AM
0 9 * * * python /path/to/web_ingest.py --url https://example.com --out /data/daily.json
```

## Output format

```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "meta_description": "",
  "headings": [{"tag": "h1", "text": "..."}],
  "links": [{"text": "...", "href": "..."}],
  "body_text": "...",
  "extracted_at": "2026-10-08T12:00:00+00:00"
}
```

## Pricing

| Package | Price | What's included |
|---------|-------|----------------|
| Single script | $500 | One custom script for one site/task, delivered with a 15-min walkthrough |
| Custom build | $750–$1,500 | Multi-step flows, scheduled runs, error handling, your branding |
| Monthly retainer | $300/mo | Ongoing maintenance, new tasks added, priority support |

**Book a 15-minute call:** I'll show you one task you do weekly and what it costs to automate.

Contact: open an issue on this repo or message @Tawns-lab on X.
