import pytest

from tests.config import TestConfig

USERS_URL = TestConfig.USERS_URL
FILES_URL = TestConfig.FILES_URL
ROLES_URL = TestConfig.ROLES_URL
PROFILES_URL = TestConfig.PROFILES_URL
DIRECTORIES_CATEGORIES_URL = TestConfig.DIRECTORIES_CATEGORIES_URL
FEEDBACKS_URL = TestConfig.FEEDBACKS_URL


@pytest.mark.parametrize("page", [1, None])
@pytest.mark.parametrize("per_page", [1, None])
@pytest.mark.parametrize("include_metadata", ["enable", None])
@pytest.mark.parametrize(
    "endpoint",
    [FILES_URL, PROFILES_URL, ROLES_URL, DIRECTORIES_CATEGORIES_URL, USERS_URL, FEEDBACKS_URL],
)
def test_endpoints__list(
    fx_app,
    fx_auth_admin,
    fx_test_file,
    fx_test_feedback,
    page: str,
    per_page: str,
    include_metadata: str,
    endpoint: str,
) -> None:
    query_string = {}
    if page:
        query_string["page"] = page
    if per_page:
        query_string["per_page"] = per_page
    if include_metadata:
        query_string["include_metadata"] = include_metadata

    r_get = fx_app.get(endpoint, headers=fx_auth_admin, query_string=query_string)
    assert r_get.status_code == 200
    assert r_get.json
    assert r_get.json["items"]
    if include_metadata:
        assert r_get.json["_metadata"]
    else:
        assert not r_get.json.get("_metadata")


@pytest.mark.parametrize("page", ["BAD_VALUE", None])
@pytest.mark.parametrize("per_page", ["BAD_VALUE", None])
@pytest.mark.parametrize("include_metadata", ["BAD_VALUE", None])
@pytest.mark.parametrize(
    "endpoint",
    [FILES_URL, PROFILES_URL, ROLES_URL, DIRECTORIES_CATEGORIES_URL, USERS_URL, FEEDBACKS_URL],
)
def test_endpoints__list__error_400(
    fx_app, fx_auth_admin, page: str, per_page: str, include_metadata: str, endpoint: str
) -> None:
    query_string = {}
    if page:
        query_string["page"] = page
    if per_page:
        query_string["per_page"] = per_page
    if include_metadata:
        query_string["include_metadata"] = include_metadata

    r_get = fx_app.get("/v1/users", headers=fx_auth_admin, query_string=query_string)
    if page or per_page or include_metadata:
        assert r_get.status_code == 400
    else:
        assert True


def test_endpoints__empty_list_items(fx_app, fx_auth_admin) -> None:
    r_get = fx_app.get(
        "/v1/articles", headers=fx_auth_admin, query_string={"author": "NOT_EXIST_AUTHOR"}
    )
    assert r_get.status_code == 200
    assert not r_get.json["items"]
