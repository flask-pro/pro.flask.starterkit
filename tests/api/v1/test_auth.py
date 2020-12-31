import base64

import pytest

from tests.config import TestConfig

ACCOUNTS_URL = TestConfig.ACCOUNTS_URL


def test_auth__crud(fx_app) -> None:
    new_user = {
        "email": "test_auth_user@test_server.ru",
        "password": "test_password",
        "mobile_phone": "71234567890",
    }
    headers = {
        "Authorization": "Basic {}".format(
            base64.b64encode(f'{new_user["email"]}:{new_user["password"]}'.encode()).decode()
        )
    }

    # Signup.
    r_signup = fx_app.post("/v1/signup", json=new_user)
    assert r_signup.status_code == 201
    assert "id" in r_signup.json
    assert r_signup.json["email"] == new_user["email"]
    assert r_signup.json["mobile_phone"] == new_user["mobile_phone"]
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
        ({"email": "BAD_EMAIL@BAD_DOMAIN.BAD"}),
        ({"password": "BAD_PASSWORD"}),
        ({"email": "BAD_EMAIL@BAD_DOMAIN.BAD", "password": "BAD_PASSWORD"}),
        ({"email": "admin", "password": "BAD_PASSWORD"}),
    ],
)
def test_auth__wrong_login_password(fx_app, payload: dict) -> None:
    headers = {
        "Authorization": "Basic {}".format(
            base64.b64encode(f'{payload.get("email")}:{payload.get("password")}'.encode()).decode()
        )
    }
    assert fx_app.post("/v1/login", headers=headers).status_code == 400


@pytest.mark.parametrize(
    "payload",
    [
        ({"email": "BAD_EMAIL@BAD_DOMAIN.BAD"}),
        ({"password": "BAD_PASSWORD"}),
        ({"email": "BAD_EMAIL@BAD_DOMAIN.BAD", "password": "BAD_PASSWORD", "BAD_KEY": "BAD_VALUE"}),
    ],
)
def test_auth__error_400(fx_app, payload: dict) -> None:
    assert fx_app.post("/v1/signup", json=payload).status_code == 400


def test_auth__double_signup(fx_app) -> None:
    new_user = {"email": "test_double_user@test_server.ru", "password": "test_password"}

    # Signup first.
    r_signup = fx_app.post("/v1/signup", json=new_user)
    assert r_signup.status_code == 201

    # Signup second.
    r_signup = fx_app.post("/v1/signup", json=new_user)
    assert r_signup.status_code == 422


def test_auth__non_auth(fx_app) -> None:
    assert fx_app.get(f"{ACCOUNTS_URL}/profile").status_code == 401


def test_auth__bad_token(fx_app) -> None:
    assert (
        fx_app.get(
            f"{ACCOUNTS_URL}/profile", headers={"Authorization": "Bearer BAD_TOKEN"}
        ).status_code
        == 401
    )
