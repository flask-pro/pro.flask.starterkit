from tests.config import TestConfig

DIRECTORIES_URL = TestConfig.DIRECTORIES_URL
DIRECTORIES_CATEGORIES_URL = TestConfig.DIRECTORIES_CATEGORIES_URL
FILES_URL = TestConfig.FILES_URL


def test_directories(fx_app, fx_auth_admin, fx_test_category, fx_test_article) -> None:
    fx_test_category("feedbacks")

    directories = fx_app.get(DIRECTORIES_URL, headers=fx_auth_admin)
    assert directories.status_code == 200
    assert directories.json["feedbacks"]["categories"]
    assert directories.json["articles"][fx_test_article["global_name"]]


def test_directories__categories_crud(
    fx_app, fx_auth_admin, fx_comparing_keys_values, fx_test_file_non_deleted
) -> None:
    new_category_data = {
        "name": "test_feedback_category_name",
        "content_type": "feedbacks",
        "icon_id": fx_test_file_non_deleted()["id"],
    }

    new_category = fx_app.post(
        DIRECTORIES_CATEGORIES_URL, headers=fx_auth_admin, json=new_category_data
    )
    assert new_category.status_code == 201
    fx_comparing_keys_values(new_category_data, new_category.json, exclude_keys=["icon_id"])
    assert new_category.json["icon"]["id"] == new_category_data["icon_id"]

    category = fx_app.get(
        f'{DIRECTORIES_CATEGORIES_URL}/{new_category.json["id"]}', headers=fx_auth_admin
    )
    assert category.status_code == 200
    fx_comparing_keys_values(new_category_data, category.json, exclude_keys=["icon_id"])
    assert category.json["icon"]["id"] == new_category_data["icon_id"]

    updated_category_data = {
        "id": new_category.json["id"],
        "name": "test_updated_category_name",
        "content_type": "articles",
        "icon_id": fx_test_file_non_deleted()["id"],
    }
    updated_category = fx_app.put(
        f'{DIRECTORIES_CATEGORIES_URL}/{new_category.json["id"]}',
        headers=fx_auth_admin,
        json=updated_category_data,
    )
    assert updated_category.status_code == 200
    fx_comparing_keys_values(updated_category_data, updated_category.json, exclude_keys=["icon_id"])
    assert updated_category.json["icon"]["id"] == updated_category_data["icon_id"]

    deleted_category = fx_app.delete(
        f'{DIRECTORIES_CATEGORIES_URL}/{new_category.json["id"]}', headers=fx_auth_admin
    )
    assert deleted_category.status_code == 204
    assert not deleted_category.data
    for file_id in [category.json["icon"]["id"], updated_category.json["icon"]["id"]]:
        assert fx_app.get(f"{FILES_URL}/{file_id}", headers=fx_auth_admin).status_code == 404
        assert (
            fx_app.get(f"{FILES_URL}/download/{file_id}", headers=fx_auth_admin).status_code == 404
        )
