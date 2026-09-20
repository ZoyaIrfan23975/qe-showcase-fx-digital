from pytest_bdd import scenarios, given, when, then, parsers
from pages.streaming_page import StreamingPage

scenarios("../features/continue_watching.feature")


@given("the streaming app is loaded", target_fixture="streaming_page")
def streaming_page(app_page):
    return StreamingPage(app_page)


@when(parsers.parse('I set progress for show "{show_id}" to {progress:d} percent'))
def set_progress(streaming_page, show_id, progress):
    streaming_page.set_progress(show_id, progress)


@then(parsers.parse('show "{show_id}" should {expectation} in the Continue Watching row'))
def check_continue_watching(streaming_page, show_id, expectation):
    is_present = streaming_page.is_in_continue_watching(show_id)
    if expectation == "appear":
        assert is_present, f"Expected show {show_id} to appear in Continue Watching"
    else:
        assert not is_present, f"Expected show {show_id} to NOT appear in Continue Watching"
