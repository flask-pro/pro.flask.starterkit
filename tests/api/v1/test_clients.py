from tests.config import TestConfig

CLIENTS_URL = TestConfig.CLIENTS_URL


def test_clients__crud(fx_app, fx_auth_admin) -> None:
    print("\n--> test_clients__crud")
    new_client_data = {
        "name": "test_client",
        "last_name": "test_client",
        "mobile_phone": "71234567890",
        "description": "test_client",
    }

    new_client = fx_app.post(CLIENTS_URL, headers=fx_auth_admin, json=new_client_data)
    assert new_client.status_code == 201
    assert "id" in new_client.json
    assert new_client.json["name"] == new_client_data["name"]
    assert new_client.json["last_name"] == new_client_data["last_name"]
    assert new_client.json["mobile_phone"] == new_client_data["mobile_phone"]
    assert new_client.json["description"] == new_client_data["description"]

    client = fx_app.get(f'{CLIENTS_URL}/{new_client.json["id"]}', headers=fx_auth_admin)
    assert client.status_code == 200
    assert client.json["id"] == new_client.json["id"]
    assert client.json["name"] == new_client_data["name"]
    assert client.json["last_name"] == new_client_data["last_name"]
    assert client.json["mobile_phone"] == new_client_data["mobile_phone"]
    assert client.json["description"] == new_client_data["description"]

    updated_client_data = {
        "id": new_client.json["id"],
        "name": "updated_test_client",
        "last_name": "updated_test_client",
        "mobile_phone": "70987654321",
        "description": "updated_test_client",
    }
    updated_client = fx_app.put(
        f'{CLIENTS_URL}/{new_client.json["id"]}', headers=fx_auth_admin, json=updated_client_data
    )
    assert updated_client.status_code == 200
    assert updated_client.json["id"] == new_client.json["id"]
    assert updated_client.json["name"] == updated_client_data["name"]
    assert updated_client.json["last_name"] == updated_client_data["last_name"]
    assert updated_client.json["mobile_phone"] == updated_client_data["mobile_phone"]
    assert updated_client.json["description"] == updated_client_data["description"]

    deleted_client = fx_app.delete(f'{CLIENTS_URL}/{new_client.json["id"]}', headers=fx_auth_admin)
    assert deleted_client.status_code == 204
    assert not deleted_client.data
