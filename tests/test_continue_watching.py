import pytest
from pages.streaming_page import StreamingPage

# Reference — show IDs defined in index.html:
# 1 = Nebula Heights      (licensed for offline)
# 2 = Coastal Detectives  (NOT licensed for offline)


# ---------------------------------------------------------------------------
# Boundary value tests — the "Continue Watching" rule is: 0 < progress < 100.
# We test exactly at and around both edges, not just a random middle value,
# because off-by-one bugs (e.g. someone writing ">=" instead of ">") hide
# exactly at boundaries.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "progress_value, should_appear",
    [
        (0, False),    # not started yet -> should NOT be in Continue Watching
        (1, True),     # just started -> SHOULD appear
        (95, True),    # nearly finished, still in progress -> SHOULD appear
        (100, False),  # fully finished -> should NOT appear
    ],
)
def test_continue_watching_boundary_values(app_page, progress_value, should_appear):
    stream = StreamingPage(app_page)
    stream.set_progress(show_id=1, value=progress_value)

    assert stream.is_in_continue_watching(1) == should_appear


# ---------------------------------------------------------------------------
# Decision table tests — the Download button requires THREE conditions to
# all be true: premium account AND storage available AND the show itself
# being licensed for offline viewing. We test the meaningful combinations,
# not just the "everything works" happy path.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "premium, storage, expected_enabled",
    [
        (True, True, True),     # all conditions met -> enabled
        (True, False, False),   # missing storage -> disabled
        (False, True, False),   # missing premium -> disabled
        (False, False, False),  # missing both -> disabled
    ],
)
def test_download_button_decision_table(app_page, premium, storage, expected_enabled):
    stream = StreamingPage(app_page)
    stream.set_premium(premium)
    stream.set_storage_available(storage)

    # Show 1 (Nebula Heights) IS licensed for offline, so its download
    # button's state depends purely on the premium/storage combination.
    assert stream.is_download_enabled(1) == expected_enabled


def test_download_button_disabled_when_show_not_licensed(app_page):
    stream = StreamingPage(app_page)
    stream.set_premium(True)
    stream.set_storage_available(True)

    # Show 2 (Coastal Detectives) is NOT licensed for offline. Even with
    # premium AND storage both true, the button must stay disabled —
    # this is the case that's easy to forget if you only test the show
    # that IS licensed.
    assert stream.is_download_enabled(2) is False


# ---------------------------------------------------------------------------
# Equivalence partitioning tests — the search box has three input "buckets"
# that should each behave consistently: empty, a matching query, and a
# non-matching query. One representative test per bucket is enough.
# ---------------------------------------------------------------------------
def test_search_empty_shows_all_shows(app_page):
    stream = StreamingPage(app_page)
    stream.search("")

    titles = stream.get_all_show_titles()
    assert len(titles) == 5


def test_search_matching_query_filters_results(app_page):
    stream = StreamingPage(app_page)
    stream.search("Nebula")

    titles = stream.get_all_show_titles()
    assert titles == ["Nebula Heights"]


def test_search_no_match_shows_empty_state_message(app_page):
    stream = StreamingPage(app_page)
    stream.search("xyz123")

    assert stream.is_no_results_message_visible()