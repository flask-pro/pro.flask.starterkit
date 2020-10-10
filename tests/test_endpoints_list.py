import pytest

from .config import TestConfig

USERS_URL = TestConfig.USERS_URL
FILES_URL = TestConfig.FILES_URL
ROLES_URL = TestConfig.ROLES_URL


@pytest.mark.parametrize("page", [1, None])
@pytest.mark.parametrize("per_page", [1, None])
@pytest.mark.parametrize("include_metadata", [True, None])
@pytest.mark.parametrize("endpoint", [FILES_URL, ROLES_URL, USERS_URL])
def test_endpoints__list(
    fx_app,
    fx_auth_admin,
    fx_test_file,
    page: str,
    per_page: str,
    include_metadata: str,
    endpoint: str,
) -> None:
    print("\n--> test_endpoints__list")

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


@pytest.mark.parametrize("page", ["BAD_VALUE", None])
@pytest.mark.parametrize("per_page", ["BAD_VALUE", None])
@pytest.mark.parametrize("include_metadata", ["BAD_VALUE", None])
@pytest.mark.parametrize("endpoint", [FILES_URL, ROLES_URL, USERS_URL])
def test_endpoints__list__error_400(
    fx_app, fx_auth_admin, page: str, per_page: str, include_metadata: str, endpoint: str
) -> None:
    print("\n--> test_endpoints__list__error_400")

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
