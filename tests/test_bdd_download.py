from pytest_bdd import scenarios, given, when, then, parsers
from pages.streaming_page import StreamingPage

scenarios("../features/download_eligibility.feature")


@given("the streaming app is loaded", target_fixture="streaming_page")
def streaming_page(app_page):
    return StreamingPage(app_page)


@when(parsers.parse("the user premium status is {premium} and storage available is {storage}"))
def set_conditions(streaming_page, premium, storage):
    streaming_page.set_premium(premium == "true")
    streaming_page.set_storage_available(storage == "true")


@then(parsers.parse('the download button for show "{show_id}" should be {expectation}'))
def check_download(streaming_page, show_id, expectation):
    is_enabled = streaming_page.is_download_enabled(show_id)
    if expectation == "enabled":
        assert is_enabled, f"Expected download for show {show_id} to be enabled"
    else:
        assert not is_enabled, f"Expected download for show {show_id} to be disabled"
