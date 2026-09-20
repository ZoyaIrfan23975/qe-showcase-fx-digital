import os
import pytest

APP_URL = "file://" + os.path.abspath("index.html")


@pytest.fixture
def app_page(page):
    """
    This fixture depends on pytest-playwright's built-in "page" fixture
    (which gives us a fresh browser tab per test).

    Before every test:
      1. Load the app.
      2. Clear localStorage so no progress/data leaks in from a previous test.
      3. Reload so the page reflects that clean state.

    This is what keeps our tests independent of each other (see Section 1:
    a test's result should never depend on what an earlier test did).
    """
    page.goto(APP_URL)
    page.evaluate("() => localStorage.clear()")
    page.reload()
    return page