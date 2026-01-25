import os
from pathlib import Path
from playwright.sync_api import sync_playwright


def before_all(context) -> None:
    """Setup before all tests."""
    context.playwright = sync_playwright().start()
    # Set HEADLESS=false to see the browser
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    context.browser = context.playwright.chromium.launch(headless=headless)

    # Create screenshots directory
    context.screenshots_dir = Path("screenshots")
    context.screenshots_dir.mkdir(exist_ok=True)


def after_all(context) -> None:
    """Cleanup after all tests."""
    context.browser.close()
    context.playwright.stop()


def before_scenario(context, scenario) -> None:
    """Setup before each scenario."""
    context.page = context.browser.new_page()
    context.scenario_name = scenario.name


def after_scenario(context, scenario) -> None:
    """Cleanup after each scenario."""
    # Take screenshot on failure
    if scenario.status == "failed":
        screenshot_name = f"{_sanitize_filename(context.scenario_name)}_FAILED.png"
        screenshot_path = context.screenshots_dir / screenshot_name
        context.page.screenshot(path=str(screenshot_path))
        print(f"Screenshot saved: {screenshot_path}")

    context.page.close()


def _sanitize_filename(name: str) -> str:
    """Sanitize filename by removing invalid characters."""
    # Replace invalid characters with underscores
    invalid_chars = '":<>|*?\r\n'
    for char in invalid_chars:
        name = name.replace(char, '_')
    # Replace spaces with underscores and collapse multiple underscores
    name = name.replace(' ', '_')
    while '__' in name:
        name = name.replace('__', '_')
    return name


def after_step(context, step) -> None:
    """Take screenshot after each step if configured."""
    # Screenshot modes:
    # - SCREENSHOT_STEPS=all: Capture all steps
    # - SCREENSHOT_STEPS=then: Capture only "Then" steps (default)
    # - SCREENSHOT_STEPS=false: No step screenshots
    screenshot_mode = os.getenv("SCREENSHOT_STEPS", "then").lower()

    should_screenshot = (
        screenshot_mode == "all" or
        (screenshot_mode == "then" and step.keyword.strip().lower() == "then")
    )

    if should_screenshot:
        # Save to screenshots directory
        step_name = f"{context.scenario_name}_{step.keyword.strip()}_{step.name}"
        screenshot_name = f"{_sanitize_filename(step_name)}.png"
        screenshot_path = context.screenshots_dir / screenshot_name
        context.page.screenshot(path=str(screenshot_path))
        print(f"Step screenshot saved: {screenshot_path}")
