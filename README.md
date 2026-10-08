# web-puller

**Playwright WebKit browser automation script.**
Logs into a site, pulls data from a target page, saves it to a file.

Built by Alttawan Hensley (Alt Tate) — https://github.com/Tawns-lab

## What it does

- Opens any URL in a headless **WebKit** browser (Playwright)
- Optionally logs in using generic form detection (username/email + password + submit)
- Extracts data via CSS selector, or pulls page title + visible body text by default
- Saves everything to a JSON file with timestamp and status

## Install

```bash
pip install -r requirements.txt
playwright install webkit
```

## Usage

```bash
# Basic pull (no login)
python web_puller.py --url https://example.com --output data.json

# Pull with login
python web_puller.py --url https://example.com --login --user me@example.com --password secret --output data.json

# Extract specific elements
python web_puller.py --url https://example.com --selector "h1, .price" --output prices.json
```

## Output format

```json
{
  "url": "https://example.com",
  "pulled_at": "2026-10-08T12:00:00+00:00",
  "status": "ok",
  "data": {
    "title": "Example Domain",
    "text": "..."
  },
  "error": null
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
