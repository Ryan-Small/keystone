import os
from playwright.sync_api import sync_playwright


def before_all(context) -> None:
    """Setup before all tests."""
    context.playwright = sync_playwright().start()
    # Set HEADLESS=false to see the browser
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    context.browser = context.playwright.chromium.launch(headless=headless)


def after_all(context) -> None:
    """Cleanup after all tests."""
    context.browser.close()
    context.playwright.stop()


def before_scenario(context, scenario) -> None:
    """Setup before each scenario."""
    context.page = context.browser.new_page()


def after_scenario(context, scenario) -> None:
    """Cleanup after each scenario."""
    context.page.close()
