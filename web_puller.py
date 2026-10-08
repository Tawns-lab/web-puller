#!/usr/bin/env python3
"""
web-puller: Playwright WebKit browser automation script.
Logs into a site, pulls data from a target page, saves it to a file.

Usage:
    python web_puller.py --url https://example.com --output data.json
    python web_puller.py --url https://example.com --login --user me@example.com --password secret --output data.json

Install:
    pip install -r requirements.txt
    playwright install webkit
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    print("ERROR: playwright not installed. Run: pip install -r requirements.txt && playwright install webkit", file=sys.stderr)
    sys.exit(1)


def pull(url, output, login=False, user=None, password=None, selector=None, timeout=30000):
    """Open url in WebKit, optionally log in, extract data, save to output."""
    result = {
        "url": url,
        "pulled_at": datetime.now(timezone.utc).isoformat(),
        "status": "ok",
        "data": None,
        "error": None,
    }

    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(timeout)

        try:
            page.goto(url, wait_until="domcontentloaded")

            if login:
                if not user or not password:
                    raise ValueError("--login requires --user and --password")
                # Generic login: fill first visible text input with user,
                # first password input with password, click first submit button
                page.locator('input[type="text"], input[type="email"], input:not([type])').first.fill(user)
                page.locator('input[type="password"]).first.fill(password)
                page.locator('button[type="submit"], input[type="submit"], button:has-text("Log in"), button:has-text("Sign in")').first.click()
                page.wait_for_load_state("domcontentloaded")

            if selector:
                elements = page.locator(selector).all()
                result["data"] = [el.inner_text().strip() for el in elements if el.inner_text().strip()]
            else:
                # Default: pull page title + all visible text blocks
                result["data"] = {
                    "title": page.title(),
                    "text": page.locator("body").inner_text()[:5000],
                }

        except PWTimeout as e:
            result["status"] = "timeout"
            result["error"] = str(e)
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        finally:
            browser.close()

    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main():
    ap = argparse.ArgumentParser(description="Playwright WebKit data puller")
    ap.add_argument("--url", required=True, help="Target URL")
    ap.add_argument("--output", default="data.json", help="Output file (default: data.json)")
    ap.add_argument("--login", action="store_true", help="Attempt login before pulling")
    ap.add_argument("--user", help="Login username/email")
    ap.add_argument("--password", help="Login password")
    ap.add_argument("--selector", help="CSS selector to extract (default: page title + body text)")
    ap.add_argument("--timeout", type=int, default=30000, help="Page timeout in ms")
    args = ap.parse_args()

    result = pull(args.url, args.output, args.login, args.user, args.password, args.selector, args.timeout)
    print(json.dumps({"status": result["status"], "output": args.output, "error": result["error"]}, indent=2))
    sys.exit(0 if result["status"] == "ok" else 1)


if __name__ == "__main__":
    main()
