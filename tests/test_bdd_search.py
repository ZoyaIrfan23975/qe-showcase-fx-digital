from pytest_bdd import scenarios, given, when, then, parsers
from pages.streaming_page import StreamingPage

scenarios("../features/search.feature")


@given("the streaming app is loaded", target_fixture="streaming_page")
def streaming_page(app_page):
    return StreamingPage(app_page)


@when(parsers.parse('I search for "{query}"'))
def search(streaming_page, query):
    streaming_page.search(query)


@then("no results message should be visible")
def check_no_results(streaming_page):
    assert streaming_page.is_no_results_message_visible()
