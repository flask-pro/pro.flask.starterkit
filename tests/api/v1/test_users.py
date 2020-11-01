def test_users__crud(fx_app, fx_auth_admin) -> None:
    print("\n--> test_users__crud")
    new_user = {"username": "test_crud_user", "password": "test_password", "role": "user"}

    r_create = fx_app.post("/v1/users", headers=fx_auth_admin, json=new_user)
    assert r_create.status_code == 201
    assert "id" in r_create.json
    assert r_create.json["username"] == new_user["username"]

    r_get = fx_app.get(f'/v1/users/{r_create.json["id"]}', headers=fx_auth_admin)
    assert r_get.status_code == 200
    assert r_get.json["id"] == r_create.json["id"]
    assert r_get.json["username"] == r_create.json["username"]

    updated_user = {"id": r_create.json["id"], "username": "updated_test_user", "role": "user"}
    r_update = fx_app.put(
        f'/v1/users/{r_create.json["id"]}', headers=fx_auth_admin, json=updated_user
    )
    assert r_update.status_code == 200
    assert r_update.json["id"] == r_create.json["id"]
    assert r_update.json["username"] == updated_user["username"]

    r_delete = fx_app.delete(f'/v1/users/{r_create.json["id"]}', headers=fx_auth_admin)
    assert r_delete.status_code == 204
    assert not r_delete.data


def test_users__bad_id(fx_app, fx_auth_admin) -> None:
    print("\n--> test_users__bad_id")

    r_get = fx_app.get("/v1/users/1234567890", headers=fx_auth_admin)
    assert r_get.status_code == 404

    updated_user = {"id": 1234567890, "username": "updated_test_user", "role": "user"}
    r_update = fx_app.put("/v1/users/1234567890", headers=fx_auth_admin, json=updated_user)
    assert r_update.status_code == 404

    r_delete = fx_app.delete("/v1/users/1234567890", headers=fx_auth_admin)
    assert r_delete.status_code == 404


def test_roles__crud(fx_app, fx_auth_admin) -> None:
    print("\n--> test_roles__crud")
    new_role = {"name": "test_crud_role", "description": "test_crud_role_description"}

    r_create = fx_app.post("/v1/roles", headers=fx_auth_admin, json=new_role)
    assert r_create.status_code == 201
    assert "id" in r_create.json
    assert r_create.json["name"] == new_role["name"]
    assert r_create.json["description"] == new_role["description"]

    r_get = fx_app.get(f'/v1/roles/{r_create.json["id"]}', headers=fx_auth_admin)
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
        f'/v1/roles/{r_create.json["id"]}', headers=fx_auth_admin, json=updated_role
    )
    assert r_update.status_code == 200
    assert r_update.json["id"] == r_create.json["id"]
    assert r_update.json["name"] == updated_role["name"]
    assert r_update.json["description"] == updated_role["description"]

    r_delete = fx_app.delete(f'/v1/roles/{r_create.json["id"]}', headers=fx_auth_admin)
    assert r_delete.status_code == 204
    assert not r_delete.data
