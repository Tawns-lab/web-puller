#!/usr/bin/env python3
"""web_ingest.py - Playwright WebKit browser automation.
Logs into sites, pulls data from target pages, saves to JSON.
Built by Alttawan Hensley (Alt Tate).
"""
import argparse
import json
import sys
from datetime import datetime, timezone

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("playwright is not installed.")
    print("Run:  pip install playwright")
    print("Then: playwright install webkit")
    sys.exit(1)


def pull(url, username=None, password=None, wait_ms=2000):
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        if username and password:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            # try common login field names
            for sel in ["input[name='username']", "input[name='email']",
                        "input[type='email']", "input[name='user']"]:
                if page.locator(sel).count():
                    page.fill(sel, username)
                    break
            for sel in ["input[name='password']", "input[type='password']"]:
                if page.locator(sel).count():
                    page.fill(sel, password)
                    break
            for sel in ["button[type='submit']", "input[type='submit']",
                        "button:has-text('Log in')", "button:has-text('Sign in')"]:
                if page.locator(sel).count():
                    page.click(sel)
                    break
            page.wait_for_timeout(wait_ms)

        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(wait_ms)

        data = {
            "url": url,
            "title": page.title(),
            "meta_description": "",
            "headings": [],
            "links": [],
            "body_text": "",
            "extracted_at": datetime.now(timezone.utc).isoformat(),
        }

        desc = page.locator("meta[name='description']").first
        if desc.count():
            data["meta_description"] = desc.get_attribute("content") or ""

        data["headings"] = [h.inner_text().strip() for h in page.locator("h1, h2, h3").all()][:20]
        data["links"] = list(dict.fromkeys(
            a.get_attribute("href") for a in page.locator("a[href]").all()
            if a.get_attribute("href")
        ))[:50]
        data["body_text"] = page.locator("body").inner_text()[:5000]

        browser.close()
        return data


def main():
    ap = argparse.ArgumentParser(description="Pull data from a web page using WebKit")
    ap.add_argument("--url", required=True, help="URL to pull")
    ap.add_argument("--out", default="data.json", help="Output JSON file")
    ap.add_argument("--username", help="Login username/email")
    ap.add_argument("--password", help="Login password")
    ap.add_argument("--wait", type=int, default=2000, help="Wait ms after load")
    args = ap.parse_args()

    data = pull(args.url, args.username, args.password, args.wait)
    with open(args.out, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {args.out}")
    print(f"Title: {data['title']}")
    print(f"Headings: {len(data['headings'])}, Links: {len(data['links'])}")


if __name__ == "__main__":
    main()
