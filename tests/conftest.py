import base64
import os
import subprocess
import time
from typing import Generator

import pytest
from flask.testing import FlaskClient

from nucleus import create_app
from tests.config import TestConfig

BASE_DIR = TestConfig.BASE_DIR
FILES_URL = TestConfig.FILES_URL
CLIENTS_URL = TestConfig.CLIENTS_URL


@pytest.fixture(scope="session")
def fx_app() -> Generator[FlaskClient, None, None]:
    """Returns a flask object for accessing application.

    :return: flask test client object
    """
    print("\n-> fx_app")

    # Run containers for tests.
    subprocess.run(
        ["make", f"--directory={BASE_DIR}/..", "test_containers_start"], stdout=subprocess.PIPE
    ).stdout.decode()

    # Init app for testing.
    app = create_app(TestConfig)
    app_context = app.app.app_context()
    app_context.push()

    with app.app.test_client() as test_client:
        yield test_client

    # Stop app for testing.
    app_context.pop()

    # Stop containers for tests.
    subprocess.run(
        ["make", f"--directory={BASE_DIR}/..", "reset"], stdout=subprocess.PIPE
    ).stdout.decode()

    print("-> Teardown fx_app.")


@pytest.fixture(scope="session")
def fx_auth_admin(fx_app) -> dict:
    """Returns a header for authorization via `admin`.

    :return: authorization header
    """
    print("\n-> fx_auth_admin")
    user = {"username": "admin", "password": "secret", "role": "admin"}
    headers = {
        "Authorization": "Basic {}".format(
            base64.b64encode(f'{user["username"]}:{user["password"]}'.encode()).decode()
        )
    }
    r = fx_app.post("/v1/login", headers=headers)
    assert r.status_code == 201

    return {"Authorization": f'Bearer {r.json["access_token"]}'}


@pytest.fixture(scope="session")
def fx_test_file(fx_app, fx_auth_admin) -> Generator[dict, None, None]:
    print("\n-> fx_test_file")
    file_path = os.path.join(BASE_DIR, "content", "floppy.jpg")
    r_post = fx_app.post(
        FILES_URL,
        headers={
            "Content-Type": "multipart/form-data",
            "Authorization": fx_auth_admin["Authorization"],
        },
        data={"file": open(file_path, "rb")},
    )
    assert r_post.status_code == 201

    yield r_post.json

    r_del = fx_app.delete(f'{FILES_URL}/{r_post.json["id"]}', headers=fx_auth_admin)
    assert r_del.status_code == 204


@pytest.fixture(scope="session")
def fx_test_client(fx_app, fx_auth_admin) -> Generator[dict, None, None]:
    print("\n-> fx_test_client")

    new_client_data = {
        "name": "fx_test_client",
        "last_name": "fx_test_client",
        "mobile_phone": "71234567890",
        "description": "fx_test_client",
    }

    new_client = fx_app.post(CLIENTS_URL, headers=fx_auth_admin, json=new_client_data)
    assert new_client.status_code == 201

    yield new_client.json

    deleted_client = fx_app.delete(f'{CLIENTS_URL}/{new_client.json["id"]}', headers=fx_auth_admin)
    assert deleted_client.status_code == 204


@pytest.fixture
def fx_search_clients(fx_app, fx_auth_admin) -> Generator[list, None, None]:
    new_clients = [
        {
            "name": "First",
            "last_name": "First_ln",
            "mobile_phone": "71111111111",
            "description": "First.",
        },
        {
            "name": "Second",
            "last_name": "Second_ln",
            "mobile_phone": "72222222222",
            "description": "First Second.",
        },
        {
            "name": "Third",
            "last_name": "Third_ln",
            "mobile_phone": "73333333333",
            "description": "First Second Third.",
        },
        {
            "name": "Fourth",
            "last_name": "Fourth_ln",
            "mobile_phone": "74444444444",
            "description": "First Second Third Fourth.",
        },
        {
            "name": "Fifth",
            "last_name": "Fifth_ln",
            "mobile_phone": "75555555555",
            "description": "First Second Third Fourth Fifth.",
        },
    ]

    created_clients = []
    for client in new_clients:
        new_client = fx_app.post(CLIENTS_URL, headers=fx_auth_admin, json=client)
        assert new_client.status_code == 201
        created_clients.append(new_client.json)

    # Must wait for new entries to be indexed.
    time.sleep(1)

    yield created_clients

    for client in created_clients:
        result = fx_app.delete(f'{CLIENTS_URL}/{client["id"]}', headers=fx_auth_admin)
        assert result.status_code == 204
