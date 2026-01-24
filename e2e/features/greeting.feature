Feature: Greeting Application
  As a user
  I want to receive personalized greetings through the UI
  So that I feel welcomed

  Scenario: Get default greeting
    Given the application is running
    When I click the greeting button without entering a name
    Then I should see "Hello World" on the page

  Scenario: Get personalized greeting
    Given the application is running
    When I enter "Alice" as my name
    And I click the greeting button
    Then I should see "Hello Alice" on the page
