"""With the site running via pnpm dev, run: python -m unittest discover -s tests

Requires Python Playwright (see scripts/requirements.txt) and playwright install chromium.
"""

import unittest

from playwright.sync_api import expect, sync_playwright


class PlaygroundTest(unittest.TestCase):
    def setUp(self):
        playwright = sync_playwright().start()
        self.addCleanup(playwright.stop)
        browser = playwright.chromium.launch()
        self.addCleanup(browser.close)
        self.page = browser.new_page()
        self.page.goto("http://127.0.0.1:5173/apidex-hub/", wait_until="domcontentloaded")
        self.endpoint = "https://catfact.ninja/fact"

    def button(self, name):
        return self.page.get_by_role("button", name=name, exact=True)

    def test_network_failure_replaces_live_response_and_can_be_retried(self):
        self.page.route(self.endpoint, lambda route: route.fulfill(json={"fact": "Live result"}))
        self.button("Test Query").click()
        expect(self.button("Success")).to_be_visible()
        expect(self.page.get_by_text("Live result", exact=False)).to_be_visible()

        self.page.route(self.endpoint, lambda route: route.abort(), times=1)
        self.button("Success").click()
        expect(self.page.get_by_role("alert")).to_contain_text("Request failed")
        expect(self.button("Success")).to_have_count(0)
        expect(self.page.get_by_text("Live result", exact=False)).to_have_count(0)
        expect(self.page.get_by_text("A cat's hearing", exact=False)).to_have_count(0)

        self.button("Retry").click()
        expect(self.button("Success")).to_be_visible()
        expect(self.page.get_by_role("alert")).to_have_count(0)

    def test_example_is_not_live_and_http_errors_show_the_status(self):
        self.button("Response").click()
        expect(self.page.get_by_text("Example response", exact=True)).to_be_visible()
        expect(self.button("Success")).to_have_count(0)

        self.page.route(self.endpoint, lambda route: route.fulfill(status=503, body="Unavailable"))
        self.button("Test Query").click()
        expect(self.page.get_by_role("alert")).to_contain_text("HTTP 503")
        expect(self.page.get_by_text("Example response", exact=True)).to_have_count(0)
