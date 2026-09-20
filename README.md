# QE Showcase - FX Digital

A small but complete QA/QE framework built around a self-contained CTV-style
streaming demo app, showing my approach to test design, automation, and CI
across manual, automated, API, and BDD testing.

## Why this project

Rather than automate an existing public demo site, I built my own minimal
"StreamDemo" app so I could deliberately design in specific, testable
behaviours (boundary conditions, decision-table logic, equivalence classes)
and demonstrate the *reasoning* behind each test, not just the test code
itself.

## Tech stack

- **Python + Playwright + pytest** - primary automation stack
- **pytest-bdd** - Gherkin/BDD layer over the same application
- **TypeScript + Playwright Test** - small secondary example (see note below)
- **GitHub Actions** - CI pipeline, runs on every push/PR

## Project structure
