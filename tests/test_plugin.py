from playwright.sync_api import Page


def test_plugin(page: Page, assert_snapshot):
    page.goto("https://example.com")
    assert_snapshot(page.screenshot(), "example.png")
    href = page.query_selector("a")
    assert_snapshot(href.screenshot(), "href.png")
