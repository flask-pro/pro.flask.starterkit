import time

import pytest

from tests.config import TestConfig

CLIENTS_URL = TestConfig.CLIENTS_URL
SEARCH_URL = TestConfig.SEARCH_URL


def test_search__crud(fx_app, fx_auth_admin) -> None:
    print("\n--> test_search__crud")

    # Create and search.
    new_client = {
        "name": "test_crud",
        "last_name": "test_crud",
        "mobile_phone": "71122334455",
        "description": "test_crud.",
    }
    new_client = fx_app.post(CLIENTS_URL, headers=fx_auth_admin, json=new_client)
    assert new_client.status_code == 201
    time.sleep(1)

    search_result = fx_app.get(
        f"{SEARCH_URL}", query_string={"scope": "clients", "q": "test_crud"}, headers=fx_auth_admin
    )
    assert search_result.status_code == 200
    assert len(search_result.json["items"]) == 1

    # Update and search.
    updated_client_data = {
        "id": new_client.json["id"],
        "name": "updated_test_crud",
        "last_name": "updated_test_crud",
        "mobile_phone": "75544332211",
        "description": "updated_test_crud",
    }
    updated_client = fx_app.put(
        f'{CLIENTS_URL}/{new_client.json["id"]}', headers=fx_auth_admin, json=updated_client_data
    )
    assert updated_client.status_code == 200
    time.sleep(1)

    search_result = fx_app.get(
        f"{SEARCH_URL}",
        query_string={"scope": "clients", "q": "updated_test_crud"},
        headers=fx_auth_admin,
    )
    assert search_result.status_code == 200
    assert len(search_result.json["items"]) == 1

    # Delete and search.
    deleted_client = fx_app.delete(f'{CLIENTS_URL}/{new_client.json["id"]}', headers=fx_auth_admin)
    assert deleted_client.status_code == 204
    time.sleep(1)

    search_result = fx_app.get(
        f"{SEARCH_URL}",
        query_string={"scope": "clients", "q": "updated_test_crud"},
        headers=fx_auth_admin,
    )
    assert search_result.status_code == 404


def test_search(fx_app, fx_auth_admin, fx_search_clients) -> None:
    print("\n--> test_search")

    search_result = fx_app.get(
        f"{SEARCH_URL}", query_string={"scope": "clients", "q": "First"}, headers=fx_auth_admin
    )
    assert search_result.status_code == 200
    assert search_result.json
    assert len(search_result.json["items"]) == 5
    assert search_result.json["items"][0]["id"]
    assert search_result.json["items"][0]["name"] == fx_search_clients[0]["name"]
    assert search_result.json["items"][0]["last_name"] == fx_search_clients[0]["last_name"]
    assert search_result.json["items"][0]["description"] == fx_search_clients[0]["description"]


def test_search__metadata(fx_app, fx_auth_admin, fx_search_clients) -> None:
    print("\n--> test_search__metadata")

    search_result = fx_app.get(
        f"{SEARCH_URL}",
        query_string={"scope": "clients", "q": "First", "include_metadata": True},
        headers=fx_auth_admin,
    )
    assert search_result.status_code == 200
    assert search_result.json["items"]
    assert search_result.json["_metadata"]


def test_search__bad_query(fx_app, fx_auth_admin, fx_search_clients) -> None:
    print("\n--> test_search__bad_query")

    search_result = fx_app.get(
        f"{SEARCH_URL}",
        query_string={"scope": "clients", "q": "NON_EXIST_QUERY"},
        headers=fx_auth_admin,
    )
    assert search_result.status_code == 404


@pytest.mark.parametrize("scope", (("users"), ("files")))
def test_search__bad_scope(fx_app, fx_auth_admin, fx_search_clients, scope) -> None:
    print("\n--> test_search__bad_scope")

    search_result = fx_app.get(
        f"{SEARCH_URL}", query_string={"scope": scope, "q": "First"}, headers=fx_auth_admin
    )
    assert search_result.status_code == 400


def test_search__reindex(fx_app, fx_auth_admin, fx_search_clients) -> None:
    print("\n--> test_search__reindex")

    search_result = fx_app.get(
        f"{SEARCH_URL}/reindex", query_string={"scope": "clients"}, headers=fx_auth_admin
    )
    assert search_result.status_code == 200
    assert search_result.data.decode() == "OK"
