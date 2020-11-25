import time

import pytest

from tests.config import TestConfig

ARTICLES_URL = TestConfig.ARTICLES_URL
SEARCH_URL = TestConfig.SEARCH_URL


def test_search__crud(fx_app, fx_auth_admin) -> None:
    print("\n--> test_search__crud")

    # Create and search.
    new_article_data = {
        "title": "test_search_title",
        "announce": "test search announce",
        "content": "test search content",
        "author": "test search author",
    }
    new_article = fx_app.post(ARTICLES_URL, headers=fx_auth_admin, json=new_article_data)
    assert new_article.status_code == 201

    # Нужно дождаться пока индекс инициализируется.
    time.sleep(1)

    search_result = fx_app.get(
        f"{SEARCH_URL}",
        query_string={"scope": "articles", "q": "test_search_title"},
        headers=fx_auth_admin,
    )
    assert search_result.status_code == 200
    assert len(search_result.json["items"]) == 1

    # Update and search.
    updated_article_data = {
        "id": new_article.json["id"],
        "title": "updated_test_search_title",
        "announce": "updated test search announce",
        "content": "updated test search content",
        "author": "updated test search author",
    }
    updated_article = fx_app.put(
        f'{ARTICLES_URL}/{new_article.json["id"]}', headers=fx_auth_admin, json=updated_article_data
    )
    assert updated_article.status_code == 200

    # Нужно дождаться пока индекс инициализируется.
    time.sleep(1)

    search_result = fx_app.get(
        f"{SEARCH_URL}",
        query_string={"scope": "articles", "q": "updated_test_search_title"},
        headers=fx_auth_admin,
    )
    assert search_result.status_code == 200
    assert len(search_result.json["items"]) == 1

    # Delete and search.
    deleted_article = fx_app.delete(
        f'{ARTICLES_URL}/{new_article.json["id"]}', headers=fx_auth_admin
    )
    assert deleted_article.status_code == 204

    # Нужно дождаться пока индекс инициализируется.
    time.sleep(1)

    search_result = fx_app.get(
        f"{SEARCH_URL}",
        query_string={"scope": "articles", "q": "updated_test_search_title"},
        headers=fx_auth_admin,
    )
    assert search_result.status_code == 404


def test_search(fx_app, fx_auth_admin, fx_search_articles) -> None:
    print("\n--> test_search")

    search_result = fx_app.get(
        f"{SEARCH_URL}", query_string={"scope": "articles", "q": "First"}, headers=fx_auth_admin
    )
    assert search_result.status_code == 200
    assert search_result.json
    assert len(search_result.json["items"]) == 1
    assert search_result.json["items"][0]["id"]
    assert search_result.json["items"][0]["title"] == fx_search_articles[0]["title"]
    assert search_result.json["items"][0]["announce"] == fx_search_articles[0]["announce"]
    assert search_result.json["items"][0]["content"] == fx_search_articles[0]["content"]
    assert search_result.json["items"][0]["author"] == fx_search_articles[0]["author"]


def test_search__metadata(fx_app, fx_auth_admin, fx_search_articles) -> None:
    print("\n--> test_search__metadata")

    search_result = fx_app.get(
        f"{SEARCH_URL}",
        query_string={"scope": "articles", "q": "First", "include_metadata": "enable"},
        headers=fx_auth_admin,
    )
    assert search_result.status_code == 200
    assert search_result.json["items"]
    assert search_result.json["_metadata"]


def test_search__bad_query(fx_app, fx_auth_admin, fx_search_articles) -> None:
    print("\n--> test_search__bad_query")

    search_result = fx_app.get(
        f"{SEARCH_URL}",
        query_string={"scope": "articles", "q": "NON_EXIST_QUERY"},
        headers=fx_auth_admin,
    )
    assert search_result.status_code == 404


@pytest.mark.parametrize("scope", (("users"), ("files")))
def test_search__bad_scope(fx_app, fx_auth_admin, fx_search_articles, scope) -> None:
    print("\n--> test_search__bad_scope")

    search_result = fx_app.get(
        f"{SEARCH_URL}", query_string={"scope": scope, "q": "First"}, headers=fx_auth_admin
    )
    assert search_result.status_code == 400


def test_search__reindex(fx_app, fx_auth_admin, fx_search_articles) -> None:
    print("\n--> test_search__reindex")

    search_result = fx_app.get(
        f"{SEARCH_URL}/reindex", query_string={"scope": "articles"}, headers=fx_auth_admin
    )
    assert search_result.status_code == 200
    assert search_result.data.decode() == "OK"
