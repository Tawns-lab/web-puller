#!/usr/bin/env python3
"""test_install.py - verify dependencies before running web_ingest.py"""
import sys

ok = True
try:
    import playwright
    print("OK  playwright", getattr(playwright, "__version__", ""))
except ImportError:
    print("FAIL playwright - run: pip install playwright")
    ok = False

try:
    from playwright.sync_api import sync_playwright
    print("OK  playwright.sync_api")
except ImportError:
    print("FAIL playwright.sync_api")
    ok = False

if ok:
    print("All checks passed. Run: python web_ingest.py --url https://example.com --out data.json")
else:
    print("Fix the FAIL lines above, then re-run this test.")
    sys.exit(1)
