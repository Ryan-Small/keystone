from behave import given, then, use_step_matcher, when

use_step_matcher("re")


@given("the application is running")
def step_app_running(context) -> None:
    context.page.goto("http://localhost:4200")
    context.page.wait_for_load_state("networkidle")


@when("I click the greeting button without entering a name")
def step_click_button_no_name(context) -> None:
    context.page.click("#greetButton")
    context.page.wait_for_selector("#greetingResult")


@when('I enter "(?P<name>.+)" as my name')
def step_enter_name(context, name: str) -> None:
    context.page.fill("#nameInput", name)


@when("I click the greeting button")
def step_click_button(context) -> None:
    context.page.click("#greetButton")
    context.page.wait_for_selector("#greetingResult")


@then('I should see "(?P<message>.+)" on the page')
def step_check_message(context, message: str) -> None:
    greeting_text = context.page.text_content("#greetingResult")
    assert greeting_text == message, f"Expected '{message}', got '{greeting_text}'"
