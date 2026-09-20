def test_get_show_by_id_returns_correct_show(api_context):
    response = api_context.get("/shows/1")

    assert response.status == 200
    body = response.json()
    assert body["id"] == 1
    assert "name" in body


def test_get_show_with_invalid_id_returns_404(api_context):
    # A clearly nonexistent show ID — checking the API's error handling,
    # not just its happy path.
    response = api_context.get("/shows/999999999")

    assert response.status == 404


def test_search_shows_returns_matching_results(api_context):
    response = api_context.get("/search/shows", params={"q": "firefly"})

    assert response.status == 200
    results = response.json()
    assert len(results) > 0

    # Each result wraps the actual show data under a "show" key —
    # confirming we're not just checking "it returned something",
    # but that the something is actually relevant to our query.
    assert any("firefly" in item["show"]["name"].lower() for item in results)


def test_search_shows_with_no_matches_returns_empty_list(api_context):
    # Equivalence partitioning applied to an API input: a query that
    # matches nothing is a distinct "bucket" worth checking explicitly,
    # same principle as the UI search box tests.
    response = api_context.get("/search/shows", params={"q": "zzzqqxxnonexistentshow123"})

    assert response.status == 200
    assert response.json() == []
    