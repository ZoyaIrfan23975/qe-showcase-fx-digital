Feature: Continue Watching row
  As a viewer
  I want the Continue Watching row to reflect my progress
  So that I can resume shows accurately

  Background:
    Given the streaming app is loaded

  Scenario Outline: Shows appear in Continue Watching based on progress boundaries
    When I set progress for show "<show_id>" to <progress> percent
    Then show "<show_id>" should <expectation> in the Continue Watching row

    Examples:
      | show_id | progress | expectation |
      | 1       | 0        | not appear  |
      | 1       | 1        | appear      |
      | 1       | 95       | appear      |
      | 1       | 100      | not appear  |
