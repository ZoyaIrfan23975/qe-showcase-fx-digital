Feature: Download eligibility
  As a subscriber
  I want the Download button only enabled when I am eligible
  So that I cannot attempt a download that will fail

  # Show 1 is licensed for offline viewing in the app's fixture data.
  # Show 2 is not licensed for offline viewing, which is what proves the
  # third branch of the decision table below.

  Background:
    Given the streaming app is loaded

  Scenario Outline: Download depends on premium status, storage, and offline licensing
    When the user premium status is <premium> and storage available is <storage>
    Then the download button for show "<show_id>" should be <expectation>

    Examples:
      | show_id | premium | storage | expectation |
      | 1       | true    | true    | enabled     |
      | 1       | true    | false   | disabled    |
      | 1       | false   | true    | disabled    |
      | 2       | true    | true    | disabled    |
