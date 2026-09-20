Feature: Show search
  As a viewer
  I want search to tell me clearly when nothing matches
  So that I am not left staring at a blank screen

  Background:
    Given the streaming app is loaded

  Scenario: Searching for a show that does not exist shows a no-results message
    When I search for "zzzznotashow"
    Then no results message should be visible
