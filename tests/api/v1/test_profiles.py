from tests.config import TestConfig

PROFILES_URL = TestConfig.PROFILES_URL


def test_profiles__crud(fx_app, fx_auth_admin) -> None:
    new_profile = {
        "name": "test_crud_name_profile",
        "lastname": "test_crud_lastname_profile",
        "description": "test_crud_profile_description",
    }

    r_create = fx_app.post(PROFILES_URL, headers=fx_auth_admin, json=new_profile)
    assert r_create.status_code == 201
    assert "id" in r_create.json
    assert r_create.json["name"] == new_profile["name"]
    assert r_create.json["lastname"] == new_profile["lastname"]
    assert r_create.json["description"] == new_profile["description"]

    r_get = fx_app.get(f'{PROFILES_URL}/{r_create.json["id"]}', headers=fx_auth_admin)
    assert r_get.status_code == 200
    assert r_get.json["id"] == r_create.json["id"]
    assert r_get.json["name"] == r_create.json["name"]
    assert r_get.json["lastname"] == r_create.json["lastname"]
    assert r_get.json["description"] == r_create.json["description"]

    updated_profile = {
        "id": r_create.json["id"],
        "name": "updated_test_name",
        "lastname": "updated_test_lastname",
        "description": "test_updated_description",
    }
    r_update = fx_app.put(
        f'{PROFILES_URL}/{r_create.json["id"]}', headers=fx_auth_admin, json=updated_profile
    )
    assert r_update.status_code == 200
    assert r_update.json["id"] == r_create.json["id"]
    assert r_update.json["name"] == updated_profile["name"]
    assert r_update.json["lastname"] == updated_profile["lastname"]
    assert r_update.json["description"] == updated_profile["description"]

    r_delete = fx_app.delete(f'{PROFILES_URL}/{r_create.json["id"]}', headers=fx_auth_admin)
    assert r_delete.status_code == 204
    assert not r_delete.data
