import base64

import pytest


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
    assert not r_signup.json.get("role")

    # Login.
    r_login = fx_app.post("/v1/login", headers=headers)
    assert r_login.status_code == 201
    assert r_login.json["access_token"]
    assert r_login.json["refresh_token"]

    # Get profile.
    r_profile = fx_app.get(
        "/v1/profile", headers={"Authorization": f'Bearer {r_login.json["access_token"]}'}
    )
    assert r_profile.status_code == 200
    assert "id" in r_profile.json
    assert r_profile.json["username"] == new_user["username"]
    assert not r_signup.json.get("role")

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
