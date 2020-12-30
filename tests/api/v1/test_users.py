import uuid

from tests.config import TestConfig

USERS_URL = TestConfig.USERS_URL
ROLES_URL = TestConfig.ROLES_URL


def test_users__crud(fx_app, fx_auth_admin) -> None:
    new_user = {"username": "test_crud_user", "password": "test_password", "role": "user"}

    r_create = fx_app.post(USERS_URL, headers=fx_auth_admin, json=new_user)
    assert r_create.status_code == 201
    assert "id" in r_create.json
    assert r_create.json["username"] == new_user["username"]

    r_get = fx_app.get(f'{USERS_URL}/{r_create.json["id"]}', headers=fx_auth_admin)
    assert r_get.status_code == 200
    assert r_get.json["id"] == r_create.json["id"]
    assert r_get.json["username"] == r_create.json["username"]

    updated_user = {"id": r_create.json["id"], "username": "updated_test_user", "role": "user"}
    r_update = fx_app.put(
        f'{USERS_URL}/{r_create.json["id"]}', headers=fx_auth_admin, json=updated_user
    )
    assert r_update.status_code == 200
    assert r_update.json["id"] == r_create.json["id"]
    assert r_update.json["username"] == updated_user["username"]

    r_delete = fx_app.delete(f'{USERS_URL}/{r_create.json["id"]}', headers=fx_auth_admin)
    assert r_delete.status_code == 204
    assert not r_delete.data


def test_users__bad_id(fx_app, fx_auth_admin) -> None:
    bad_uuid = str(uuid.uuid4())

    r_get = fx_app.get(f"{USERS_URL}/{bad_uuid}", headers=fx_auth_admin)
    assert r_get.status_code == 404

    updated_user = {"id": bad_uuid, "username": "updated_test_user", "role": "user"}
    r_update = fx_app.put(f"{USERS_URL}/{bad_uuid}", headers=fx_auth_admin, json=updated_user)
    assert r_update.status_code == 404

    r_delete = fx_app.delete(f"{USERS_URL}/{bad_uuid}", headers=fx_auth_admin)
    assert r_delete.status_code == 404


def test_roles__crud(fx_app, fx_auth_admin) -> None:
    new_role = {"name": "test_crud_role", "description": "test_crud_role_description"}

    r_create = fx_app.post(ROLES_URL, headers=fx_auth_admin, json=new_role)
    assert r_create.status_code == 201
    assert "id" in r_create.json
    assert r_create.json["name"] == new_role["name"]
    assert r_create.json["description"] == new_role["description"]

    r_get = fx_app.get(f'{ROLES_URL}/{r_create.json["id"]}', headers=fx_auth_admin)
    assert r_get.status_code == 200
    assert r_get.json["id"] == r_create.json["id"]
    assert r_get.json["name"] == r_create.json["name"]
    assert r_get.json["description"] == r_create.json["description"]

    updated_role = {
        "id": r_create.json["id"],
        "name": "updated_test_role",
        "description": "test_updated_role_description",
    }
    r_update = fx_app.put(
        f'{ROLES_URL}/{r_create.json["id"]}', headers=fx_auth_admin, json=updated_role
    )
    assert r_update.status_code == 200
    assert r_update.json["id"] == r_create.json["id"]
    assert r_update.json["name"] == updated_role["name"]
    assert r_update.json["description"] == updated_role["description"]

    r_delete = fx_app.delete(f'{ROLES_URL}/{r_create.json["id"]}', headers=fx_auth_admin)
    assert r_delete.status_code == 204
    assert not r_delete.data


def test_users__block(fx_app, fx_auth_admin, fx_test_user) -> None:
    user, headers, tokens, new_user_data = fx_test_user

    # User block.
    blocked_user = fx_app.put(f'{USERS_URL}/{user["id"]}/block', headers=fx_auth_admin)
    assert blocked_user.status_code == 200
    assert blocked_user.json["is_blocked"]

    # Login.
    login_result = fx_app.post("/v1/login", headers=headers)
    assert login_result.status_code == 401
    assert login_result.json["title"] == "Unauthorized"

    # Renew token.
    login_result = fx_app.put(
        "/v1/renew", headers={"Authorization": f'Bearer {tokens["refresh_token"]}'}
    )
    assert login_result.status_code == 401
    assert login_result.json["title"] == "Unauthorized"

    # Get profile.
    profile = fx_app.get(
        "/v1/accounts/profile", headers={"Authorization": f'Bearer {tokens["access_token"]}'}
    )
    assert profile.status_code == 401
    assert login_result.json["title"] == "Unauthorized"

    # User unblock.
    unblocked_user = fx_app.put(f'{USERS_URL}/{user["id"]}/unblock', headers=fx_auth_admin)
    assert unblocked_user.status_code == 200
    assert not unblocked_user.json["is_blocked"]

    # Login.
    login_result = fx_app.post("/v1/login", headers=headers)
    assert login_result.status_code == 201

    # Renew token.
    login_result = fx_app.put(
        "/v1/renew", headers={"Authorization": f'Bearer {tokens["refresh_token"]}'}
    )
    assert login_result.status_code == 201

    # Get profile.
    profile = fx_app.get(
        "/v1/accounts/profile", headers={"Authorization": f'Bearer {tokens["access_token"]}'}
    )
    assert profile.status_code == 200
