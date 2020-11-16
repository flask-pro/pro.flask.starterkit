import base64

import pytest

from tests.config import TestConfig

ACCOUNTS_URL = TestConfig.ACCOUNTS_URL


def test_auth__crud(fx_app) -> None:
    print("\n--> test_auth__crud")
    new_user = {"username": "test_auth_user", "password": "test_password"}
    headers = {
        "Authorization": "Basic {}".format(
            base64.b64encode(f'{new_user["username"]}:{new_user["password"]}'.encode()).decode()
        )
    }

    # Signup.
    r_signup = fx_app.post("/v1/signup", json=new_user)
    assert r_signup.status_code == 201
    assert "id" in r_signup.json
    assert r_signup.json["username"] == new_user["username"]
    assert r_signup.json["role"] == "user"
    assert r_signup.json["profile_id"]

    # Login.
    r_login = fx_app.post("/v1/login", headers=headers)
    assert r_login.status_code == 201
    assert r_login.json["access_token"]
    assert r_login.json["refresh_token"]

    # Renew.
    r_renew = fx_app.put(
        "/v1/renew", headers={"Authorization": f'Bearer {r_login.json["access_token"]}'}
    )
    assert r_renew.status_code == 201
    assert r_renew.json["access_token"]
    assert r_renew.json["refresh_token"]


@pytest.mark.parametrize(
    "payload",
    [
        ({"username": "BAD_USER"}),
        ({"password": "BAD_PASSWORD"}),
        ({"username": "BAD_USER", "password": "BAD_PASSWORD"}),
        ({"username": "admin", "password": "BAD_PASSWORD"}),
    ],
)
def test_auth__wrong_login_password(fx_app, payload: dict) -> None:
    print("\n--> test_auth__wrong_login_password")
    headers = {
        "Authorization": "Basic {}".format(
            base64.b64encode(
                f'{payload.get("username")}:{payload.get("password")}'.encode()
            ).decode()
        )
    }
    assert fx_app.post("/v1/login", headers=headers).status_code == 400


@pytest.mark.parametrize(
    "payload",
    [
        ({"username": "BAD_USER"}),
        ({"password": "BAD_PASSWORD"}),
        ({"username": "BAD_USER", "password": "BAD_PASSWORD", "BAD_KEY": "BAD_VALUE"}),
    ],
)
def test_auth__error_400(fx_app, payload: dict) -> None:
    print("\n--> test_auth__error_400")
    assert fx_app.post("/v1/signup", json=payload).status_code == 400


def test_auth__double_signup(fx_app) -> None:
    print("\n--> test_auth__double_signup")
    new_user = {"username": "test_double_user", "password": "test_password"}

    # Signup first.
    r_signup = fx_app.post("/v1/signup", json=new_user)
    assert r_signup.status_code == 201

    # Signup second.
    r_signup = fx_app.post("/v1/signup", json=new_user)
    assert r_signup.status_code == 422


def test_auth__non_auth(fx_app) -> None:
    print("\n--> test_auth__non_auth")
    assert fx_app.get(f"{ACCOUNTS_URL}/profile").status_code == 401


def test_auth__bad_token(fx_app) -> None:
    print("\n--> test_auth__bad_token")
    assert (
        fx_app.get(
            f"{ACCOUNTS_URL}/profile", headers={"Authorization": "Bearer BAD_TOKEN"}
        ).status_code
        == 401
    )
