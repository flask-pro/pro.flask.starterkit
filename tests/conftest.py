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
ARTICLES_URL = TestConfig.ARTICLES_URL


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
def fx_comparing_keys_values(fx_app, fx_auth_admin) -> ():
    """Проверка идентичности значений ключей двух словарей.

    :return: функция _comparing(request_data: dict, response_data: dict, exclude_keys: list)
    """
    print("\n-> fx_comparing_key_values")

    def _comparing(request_data: dict, response_data: dict, exclude_keys: list = []) -> None:
        """Проверка идентичности значений ключей двух словарей.

        :param request_data: исходный словарь.
        :param response_data: итоговый словарь.
        :param exclude_keys: ключи исключаемые из сравнения, для исходного словаря.
        :return: None
        """
        for key, value in request_data.items():
            if key not in exclude_keys:
                assert value == response_data[key]

    return _comparing


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
def fx_test_file_non_deleted(fx_app, fx_auth_admin) -> ():
    print("\n-> fx_test_file_non_delete")

    def _upload_picture() -> dict:
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
        return r_post.json

    return _upload_picture


@pytest.fixture
def fx_search_articles(fx_app, fx_auth_admin) -> Generator[list, None, None]:
    new_articles = [
        {
            "title": "First title",
            "announce": "First announce",
            "content": "First content.",
            "author": "First author",
        },
        {
            "title": "Second title",
            "announce": "Second announce",
            "content": "Second content.",
            "author": "Second author",
        },
    ]

    created_articles = []
    for article in new_articles:
        new_article = fx_app.post(ARTICLES_URL, headers=fx_auth_admin, json=article)
        assert new_article.status_code == 201
        created_articles.append(new_article.json)

    # Must wait for new entries to be indexed.
    time.sleep(1)

    yield created_articles

    for article in created_articles:
        result = fx_app.delete(f'{ARTICLES_URL}/{article["id"]}', headers=fx_auth_admin)
        assert result.status_code == 204


@pytest.fixture(scope="session")
def fx_test_article(fx_app, fx_auth_admin, fx_test_file_non_deleted) -> Generator[dict, None, None]:
    print("\n-> fx_test_article")

    new_article_data = {
        "title": "fx test article title",
        "announce": "fx test article announce",
        "content": "fx test article content",
        "main_picture_id": fx_test_file_non_deleted()["id"],
        "main_video_id": fx_test_file_non_deleted()["id"],
        "author": "fx test article author",
        "author_picture_id": fx_test_file_non_deleted()["id"],
        "global_name": "fx_test_global_name",
    }

    new_article = fx_app.post(ARTICLES_URL, headers=fx_auth_admin, json=new_article_data)
    assert new_article.status_code == 201

    yield new_article.json

    deleted_article = fx_app.delete(
        f'{ARTICLES_URL}/{new_article.json["id"]}', headers=fx_auth_admin
    )
    assert deleted_article.status_code == 204
