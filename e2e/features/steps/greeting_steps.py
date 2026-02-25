from behave import given, then, use_step_matcher, when

use_step_matcher("re")


@given("the application is running")
def step_app_running(context) -> None:
    """Navigate to the app and wait for initial load to complete."""
    context.page.goto("http://localhost:4200")
    context.page.wait_for_load_state("networkidle")


@when("I click the greeting button without entering a name")
def step_click_button_no_name(context) -> None:
    """Click the greet button with an empty name field to trigger the default greeting."""
    with context.page.expect_response(lambda r: "/api" in r.url):
        context.page.click("#greetButton")
    context.page.wait_for_selector("#greetingResult")


@when('I enter "(?P<name>.+)" as my name')
def step_enter_name(context, name: str) -> None:
    """Fill the name input field with the provided value."""
    context.page.fill("#nameInput", name)


@when("I click the greeting button")
def step_click_button(context) -> None:
    """Click the greet button and wait for the API response to render."""
    with context.page.expect_response(lambda r: "/api" in r.url):
        context.page.click("#greetButton")
    context.page.wait_for_selector("#greetingResult")


@then('I should see "(?P<message>.+)" on the page')
def step_check_message(context, message: str) -> None:
    """Assert that the greeting result element displays the expected message."""
    greeting_text = context.page.text_content("#greetingResult")
    assert greeting_text == message, f"Expected '{message}', got '{greeting_text}'"
