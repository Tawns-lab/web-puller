#!/usr/bin/env python3
"""
web_ingest.py — Playwright WebKit content ingestion engine.

Logs into a site, navigates to a target URL, extracts structured data
(title, meta description, headings, links, body text), and saves it as
JSON. Designed as a sellable automation module: swap the config, run it.

Usage:
    pip install playwright
    playwright install webkit
    python web_ingest.py --url https://example.com --out data.json

    # With login:
    python web_ingest.py --url https://example.com/dashboard \
        --login-url https://example.com/login \
        --username you@example.com --password secret \
        --out data.json

    # Scheduled (cron):
    0 9 * * * python /path/to/web_ingest.py --url ... --out /data/daily.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && playwright install webkit", file=sys.stderr)
    sys.exit(1)


def extract_page(page) -> dict[str, Any]:
    """Pull structured content from the current page."""
    data: dict[str, Any] = {
        "url": page.url,
        "title": page.title(),
        "meta_description": "",
        "headings": [],
        "links": [],
        "body_text": "",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
    }

    # Meta description
    try:
        desc = page.locator('meta[name="description"]')
        if desc.count() > 0:
            data["meta_description"] = desc.first.get_attribute("content") or ""
    except Exception:
        pass

    # Headings (h1-h3), capped
    try:
        for tag in ("h1", "h2", "h3"):
            for el in page.locator(tag).all()[:20]:
                text = el.inner_text().strip()
                if text:
                    data["headings"].append({"tag": tag, "text": text})
    except Exception:
        pass

    # Links (capped)
    try:
        for a in page.locator("a[href]").all()[:100]:
            href = a.get_attribute("href") or ""
            text = a.inner_text().strip()
            if href:
                data["links"].append({"text": text, "href": href})
    except Exception:
        pass

    # Body text, cleaned
    try:
        body = page.locator("body").inner_text()
        data["body_text"] = " ".join(body.split())[:5000]
    except Exception:
        pass

    return data


def login(page, login_url: str, username: str, password: str, timeout: int) -> None:
    """Generic login: fill first visible text/password inputs and submit."""
    page.goto(login_url, wait_until="domcontentloaded", timeout=timeout)
    page.fill('input[type="text"], input[type="email"]', username)
    page.fill('input[type="password"]', password)
    submitted = False
    for sel in ('button[type="submit"]', 'input[type="submit"]', 'button:has-text("Log in")', 'button:has-text("Sign in")'):
        try:
            if page.locator(sel).count() > 0:
                page.click(sel)
                submitted = True
                break
        except Exception:
            continue
    if not submitted:
        page.keyboard.press("Enter")
    page.wait_for_load_state("domcontentloaded", timeout=timeout)


def run(args: argparse.Namespace) -> int:
    timeout = args.timeout * 1000
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=not args.headed)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        try:
            if args.login_url and args.username and args.password:
                login(page, args.login_url, args.username, args.password, timeout)

            page.goto(args.url, wait_until="domcontentloaded", timeout=timeout)
            page.wait_for_timeout(args.wait * 1000)

            data = extract_page(page)

            out = Path(args.out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

            print(f"OK  -> {out.resolve()}")
            print(f"    title: {data['title'][:80]}")
            print(f"    headings: {len(data['headings'])} | links: {len(data['links'])}")
            return 0

        except PWTimeout as e:
            print(f"TIMEOUT: {e}", file=sys.stderr)
            return 2
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        finally:
            browser.close()


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Playwright WebKit web content ingestion engine")
    ap.add_argument("--url", required=True, help="Target URL to ingest")
    ap.add_argument("--out", default="data.json", help="Output JSON file path")
    ap.add_argument("--login-url", default=None, help="Login page URL (optional)")
    ap.add_argument("--username", default=None, help="Login username/email")
    ap.add_argument("--password", default=None, help="Login password")
    ap.add_argument("--timeout", type=int, default=30, help="Page timeout in seconds")
    ap.add_argument("--wait", type=float, default=2.0, help="Extra wait after load (seconds)")
    ap.add_argument("--headed", action="store_true", help="Show the browser window")
    return ap


if __name__ == "__main__":
    sys.exit(run(build_parser().parse_args()))
