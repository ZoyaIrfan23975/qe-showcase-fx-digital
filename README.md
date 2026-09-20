# QE Showcase - FX Digital

A complete Quality Engineering framework built around a self-contained,
CTV-style streaming demo app ("StreamDemo"). It covers automated UI testing,
API testing, BDD/Gherkin, manual/exploratory testing, and CI - with the
reasoning behind every decision documented, not just the code.

---

## 1. Why this project exists

FX Digital's interview process asks candidates to bring a working QE
framework and explain it live. Rather than automate an existing public demo
site (which is unstable and out of my control), I built my own minimal
single-page app, "StreamDemo," so I could:

- Deliberately design specific, testable behaviours (boundary conditions,
  decision-table logic, equivalence classes) into the app itself
- Fully own and explain every line of the system under test, not just the
  tests
- Theme it around streaming/CTV to match FX Digital's business as a
  Connected TV / streaming agency

---

## 2. Tech stack

- **Python + Playwright + pytest** - primary automation stack
- **pytest-bdd** - Gherkin/BDD layer over the same application
- **TypeScript + Playwright Test** - small secondary example (see section 8)
- **GitHub Actions** - CI pipeline, runs on every push/PR

---

## 3. The app under test: StreamDemo

`index.html` is a single, self-contained HTML file (no backend, no build
step) that behaves like a simplified streaming platform:

- **5 shows**, hardcoded, each with an id, title, and a `licensedOffline`
  flag (3 are licensed for offline download, 2 are not)
- **Continue Watching row** - shows any title with progress strictly
  between 0% and 100%, stored per-show in `localStorage`
- **Download button** - only enabled when three conditions are ALL true:
  the user is Premium, storage is available, AND the show is licensed for
  offline viewing
- **Search box** - filters shows by title, shows a "no results" message
  when nothing matches
- Every interactive element carries a stable `data-testid` attribute
  (e.g. `data-testid="download-btn-1"`) rather than relying on CSS
  classes or visible text - this is deliberate, since text and styling
  change often in real products but test IDs are meant to stay stable

This app was designed so that three classic test design techniques would
have a natural, real place to live:

| Technique | Where it lives in the app |
|---|---|
| Boundary value analysis | Continue Watching row (progress 0/1/95/100%) |
| Decision table testing | Download button (premium x storage x licensing) |
| Equivalence partitioning | Search box (match / no-match / empty query) |

---
## 4. Project structure
​```
index.html                     StreamDemo app (system under test)
pages/streaming_page.py        Page Object Model - Python
pytest.ini                     pytest config (test discovery, pythonpath)

tests/
  conftest.py                  Fixtures: app_page (browser), api_context (API)
  test_continue_watching.py    Boundary value + decision table + equivalence tests
  test_api.py                  Tests against the real TVMaze public API
  test_bdd_continue_watching.py  Step defs for continue_watching.feature
  test_bdd_download.py           Step defs for download_eligibility.feature
  test_bdd_search.py             Step defs for search.feature

features/
  continue_watching.feature    Gherkin - boundary values, plain English
  download_eligibility.feature Gherkin - decision table, plain English
  search.feature               Gherkin - equivalence partitioning, plain English

MANUAL_TESTS.md               6 manual/exploratory test cases + reasoning

ts-example/                   Small TypeScript/Playwright port (see section 8)
  pages/streaming-page.ts
  tests/streaming.spec.ts
  playwright.config.ts

.github/workflows/tests.yml   CI pipeline - runs full Python suite on every push
​```

---

## 5. Automated UI tests (Python + Playwright + pytest)

**File:** `tests/test_continue_watching.py` (12 test executions)

- **Boundary value analysis** - tests progress at 0%, 1%, 95%, and 100% to
  check the row's edges behave correctly (0 and 100 should NOT appear;
  1 and 95 should)
- **Decision table testing** - tests every meaningful combination of
  premium x storage x licensing for the Download button, including the
  case where premium AND storage are both true but the show still isn't
  licensed - proving the third condition is actually being checked, not
  just assumed
- **Equivalence partitioning** - tests the search box with an empty query,
  a query that matches, and a query that matches nothing, rather than
  testing every possible string

**Design decisions worth explaining in the interview:**
- **Page Object Model** (`pages/streaming_page.py`) - all `data-testid`
  selectors live in one class, so if the UI changes, only this file needs
  updating, not every test
- **Test independence** - the `app_page` fixture in `conftest.py` clears
  `localStorage` and reloads before every test, so tests never depend on
  each other's leftover state
- **`data-testid` over CSS/text selectors** - resilient to visual redesigns

---

## 6. API tests (Python + Playwright's APIRequestContext)

**File:** `tests/test_api.py` (4 tests, against the real TVMaze public API)

- Get a show by ID (200, correct fields)
- Get an invalid ID (404)
- Search with a query that matches (200, relevant result)
- Search with a query that matches nothing (200, empty list) - equivalence
  partitioning applied to API input, not just UI input

**Design decision:** the `api_context` fixture in `conftest.py` is scoped
`session` rather than `function` (like the browser fixture is) - deliberately,
since there's no per-test state risk with a stateless API context, so
re-creating it before every single test would just be wasted setup time.

---

## 7. BDD / Gherkin layer (pytest-bdd)

**Files:** `features/*.feature` (Gherkin) + `tests/test_bdd_*.py` (step definitions)

This expresses the exact same three test design techniques from section 5
again, but in Gherkin - the plain-English `Given/When/Then` format used in
Behaviour-Driven Development, so that a non-technical stakeholder (a product
owner, a client) could read the test intent without knowing Python.

- `pytest-bdd`'s `scenarios(...)` function loads a `.feature` file and turns
  each Gherkin scenario into a real pytest test at run time
- `@given` / `@when` / `@then` decorators bind plain-English lines to actual
  Playwright code
- `parsers.parse(...)` extracts values out of the Gherkin text itself (e.g.
  `<show_id>`, `<progress>`) so one line of Gherkin can drive many test runs
  via a `Scenario Outline` + `Examples` table

**Why this matters as a talking point:** it shows the underlying test design
technique (boundary value, decision table, equivalence partitioning) isn't
tied to one syntax or tool - the same reasoning can be expressed as plain
pytest or as living-documentation Gherkin, depending on the audience.

---

## 8. TypeScript example (small, honest, secondary)

**Folder:** `ts-example/`

Python is my strongest language and the focus of this repo. This folder is a
small, deliberately limited port of the core suite (9 tests: the same
boundary values and decision table cases) to TypeScript + Playwright Test,
showing that the underlying approach - Page Object Model, boundary values,
decision tables - transfers across languages. It is not meant to claim the
same depth of TypeScript experience as the Python work above.

---

## 9. Manual / exploratory testing

**File:** `MANUAL_TESTS.md`

6 test cases for things that are either genuinely hard to automate
meaningfully, or require human judgement rather than a pass/fail assertion -
for example, whether a keyboard focus outline is actually visible enough on
a dark background, or whether a CTV app has real D-pad/arrow-key navigation
(spoiler: this app currently doesn't, which is documented as a real, honest
finding rather than a fabricated pass). Each case explains WHY it's manual,
not just what to check - that reasoning is the actual point of the file.

---

## 10. CI/CD (GitHub Actions)

**File:** `.github/workflows/tests.yml`

Every push or pull request to the `master` branch automatically:
1. Checks out the code
2. Sets up Python 3.11
3. Installs pytest, Playwright, pytest-playwright, and pytest-bdd
4. Installs the Chromium browser
5. Runs the full pytest suite
6. On any failure, uploads screenshots, video, and a Playwright trace file
   as a downloadable artifact - so a failure can be debugged without
   needing to reproduce it locally first

See the repo's **Actions** tab for run history.

---

## 11. How to run everything locally

**Python suite (UI + API + BDD, 25 tests total):**

## 4. Project structure
