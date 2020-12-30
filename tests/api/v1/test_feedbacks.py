from faker import Faker

from tests.config import TestConfig

FEEDBACKS_URL = TestConfig.FEEDBACKS_URL

fake = Faker(["ru_RU"])


def test_feedbacks__crud(
    fx_app, fx_auth_admin, fx_test_file_non_deleted, fx_comparing_keys_values, fx_test_category
) -> None:
    new_feedback_data = {
        "category_id": fx_test_category("feedbacks")["id"],
        "email": fake.email(),
        "mobile_phone": "71234567890",
        "title": fake.sentence(),
        "message": fake.text(max_nb_chars=250),
    }
    new_feedback = fx_app.post(FEEDBACKS_URL, headers=fx_auth_admin, json=new_feedback_data)
    assert new_feedback.status_code == 201
    assert "id" in new_feedback.json
    fx_comparing_keys_values(new_feedback_data, new_feedback.json)

    feedback = fx_app.get(f'{FEEDBACKS_URL}/{new_feedback.json["id"]}', headers=fx_auth_admin)
    assert feedback.status_code == 200
    assert feedback.json["id"] == new_feedback.json["id"]
    fx_comparing_keys_values(new_feedback_data, feedback.json)

    updated_feedback_data = {
        "id": new_feedback.json["id"],
        "category_id": fx_test_category("feedbacks")["id"],
        "email": fake.email(),
        "mobile_phone": "71234567890",
        "title": fake.sentence(),
        "message": fake.text(max_nb_chars=250),
    }
    updated_feedback = fx_app.put(
        f'{FEEDBACKS_URL}/{new_feedback.json["id"]}',
        headers=fx_auth_admin,
        json=updated_feedback_data,
    )
    assert updated_feedback.status_code == 200
    fx_comparing_keys_values(updated_feedback_data, updated_feedback.json)

    deleted_feedback = fx_app.delete(
        f'{FEEDBACKS_URL}/{new_feedback.json["id"]}', headers=fx_auth_admin
    )
    assert deleted_feedback.status_code == 204
    assert not deleted_feedback.data


def test_feedbacks__filter(fx_app, fx_auth_admin, fx_test_feedback) -> None:
    result_filter_by_category_id = fx_app.get(
        FEEDBACKS_URL,
        headers=fx_auth_admin,
        query_string={"category_id": fx_test_feedback["category_id"]},
    )
    assert result_filter_by_category_id.status_code == 200
    assert len(result_filter_by_category_id.json["items"]) == 1
