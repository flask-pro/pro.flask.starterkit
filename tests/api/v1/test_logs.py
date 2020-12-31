from tests.config import TestConfig

LOGS_URL = TestConfig.LOGS_URL
USERS_URL = TestConfig.USERS_URL


def test_logs(fx_app, fx_auth_admin) -> None:
    logs = fx_app.get(LOGS_URL, headers=fx_auth_admin)
    assert logs.status_code == 200
    assert logs.json["items"]
    assert logs.json["items"][0]["id"]
    assert logs.json["items"][0]["email"]
    assert logs.json["items"][0]["event"]
    assert logs.json["items"][0]["message"]
    assert logs.json["items"][0]["datetime_created"]


def test_logs__filter_event(fx_app, fx_auth_admin) -> None:
    # Signup.
    new_user = {"email": "user_test_logs@nucleus.test", "password": "test_password"}
    user_signup = fx_app.post("/v1/signup", json=new_user)
    assert user_signup.status_code == 201

    result_filter_by_event_registration = fx_app.get(
        LOGS_URL,
        headers=fx_auth_admin,
        query_string={"email": new_user["email"], "event": "user_signup"},
    )
    assert result_filter_by_event_registration.status_code == 200
    assert len(result_filter_by_event_registration.json["items"]) == 1
    assert result_filter_by_event_registration.json["items"][0]["event"] == "user_signup"

    result_filter_by_event_create = fx_app.get(
        LOGS_URL,
        headers=fx_auth_admin,
        query_string={"email": new_user["email"], "event": "user_created"},
    )
    assert result_filter_by_event_create.status_code == 200
    assert len(result_filter_by_event_create.json["items"]) == 1
    assert result_filter_by_event_create.json["items"][0]["event"] == "user_created"

    # User block.
    blocked_user = fx_app.put(f'{USERS_URL}/{user_signup.json["id"]}/block', headers=fx_auth_admin)
    assert blocked_user.status_code == 200
    assert blocked_user.json["is_blocked"]

    result_filter_by_event_block = fx_app.get(
        LOGS_URL,
        headers=fx_auth_admin,
        query_string={"email": new_user["email"], "event": "user_blocked"},
    )
    assert result_filter_by_event_block.status_code == 200
    assert len(result_filter_by_event_block.json["items"]) == 1
    assert result_filter_by_event_block.json["items"][0]["event"] == "user_blocked"

    # User unblock.
    unblocked_user = fx_app.put(
        f'{USERS_URL}/{user_signup.json["id"]}/unblock', headers=fx_auth_admin
    )
    assert unblocked_user.status_code == 200
    assert not unblocked_user.json["is_blocked"]

    result_filter_by_event_unblock = fx_app.get(
        LOGS_URL,
        headers=fx_auth_admin,
        query_string={"email": new_user["email"], "event": "user_unblocked"},
    )
    assert result_filter_by_event_unblock.status_code == 200
    assert len(result_filter_by_event_unblock.json["items"]) == 1
    assert result_filter_by_event_unblock.json["items"][0]["event"] == "user_unblocked"

    # User delete.
    deleted_user = fx_app.delete(f'{USERS_URL}/{user_signup.json["id"]}', headers=fx_auth_admin)
    assert deleted_user.status_code == 204
    assert not deleted_user.data

    result_filter_by_event_delete = fx_app.get(
        LOGS_URL,
        headers=fx_auth_admin,
        query_string={"email": new_user["email"], "event": "user_deleted"},
    )
    assert result_filter_by_event_delete.status_code == 200
    assert len(result_filter_by_event_delete.json["items"]) == 1
    assert result_filter_by_event_delete.json["items"][0]["event"] == "user_deleted"


def test_logs__interval_filter(fx_app, fx_auth_admin) -> None:
    # Signup.
    new_user = {"email": "user_test_logs_interval_filter@nucleus.test", "password": "test_password"}
    user_signup = fx_app.post("/v1/signup", json=new_user)
    assert user_signup.status_code == 201

    # User delete.
    deleted_user = fx_app.delete(f'{USERS_URL}/{user_signup.json["id"]}', headers=fx_auth_admin)
    assert deleted_user.status_code == 204
    assert not deleted_user.data

    start_datetime_created = fx_app.get(
        LOGS_URL,
        headers=fx_auth_admin,
        query_string={"email": new_user["email"], "event": "user_created"},
    ).json["items"][0]["datetime_created"]

    result_filter_by_event_delete = fx_app.get(
        LOGS_URL,
        headers=fx_auth_admin,
        query_string={
            "start_datetime_created": start_datetime_created,
            "end_datetime_created": "2050-12-31T23:59:59.000000Z",
        },
    )
    assert result_filter_by_event_delete.status_code == 200
    assert len(result_filter_by_event_delete.json["items"]) == 3


def test_logs__sorted(fx_app, fx_auth_admin, fx_test_user) -> None:
    result_sorted_asc = fx_app.get(
        LOGS_URL, headers=fx_auth_admin, query_string={"sort_datetime_created": "asc"}
    )
    assert result_sorted_asc.status_code == 200

    result_sorted_desc = fx_app.get(
        LOGS_URL, headers=fx_auth_admin, query_string={"sort_datetime_created": "desc"}
    )
    assert result_sorted_desc.status_code == 200

    assert result_sorted_asc.json["items"][0] != result_sorted_desc.json["items"][0]
