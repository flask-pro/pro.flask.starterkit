import base64
import os
import subprocess
import time
from typing import Any
from typing import Generator

import pytest
from faker import Faker
from flask.testing import FlaskClient

from nucleus import create_app
from tests.config import TestConfig

BASE_DIR = TestConfig.BASE_DIR
FILES_URL = TestConfig.FILES_URL
DIRECTORIES_CATEGORIES_URL = TestConfig.DIRECTORIES_CATEGORIES_URL
ARTICLES_URL = TestConfig.ARTICLES_URL
FEEDBACKS_URL = TestConfig.FEEDBACKS_URL
USERS_URL = TestConfig.USERS_URL

fake = Faker(["ru_RU"])


@pytest.fixture(scope="session")
def fx_app() -> Generator[FlaskClient, None, None]:
    """Returns a flask object for accessing application.

    :return: flask test client object
    """

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


@pytest.fixture(scope="session")
def fx_auth_admin(fx_app) -> dict:
    """Returns a header for authorization via `admin`.

    :return: authorization header
    """
    user = {"username": "admin", "password": "secret", "role": "admin"}
    headers = {
        "Authorization": "Basic {}".format(
            base64.b64encode(f'{user["username"]}:{user["password"]}'.encode()).decode()
        )
    }
    r = fx_app.post("/v1/login", headers=headers)
    assert r.status_code == 201

    return {"Authorization": f'Bearer {r.json["access_token"]}'}


@pytest.fixture
def fx_comparing_keys_values(fx_app, fx_auth_admin) -> ():
    """Проверка идентичности значений ключей двух словарей.

    :return: функция _comparing(request_data: dict, response_data: dict, exclude_keys: list)
    """

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


@pytest.fixture
def fx_test_file(fx_app, fx_auth_admin) -> Generator[dict, None, None]:
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


@pytest.fixture
def fx_test_file_non_deleted(fx_app, fx_auth_admin) -> Any:
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
def fx_test_article(fx_app, fx_auth_admin, fx_test_file_non_deleted) -> Generator[dict, None, None]:
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
        new_client = fx_app.post(ARTICLES_URL, headers=fx_auth_admin, json=article)
        assert new_client.status_code == 201
        created_articles.append(new_client.json)

    # Must wait for new entries to be indexed.
    time.sleep(1)

    yield created_articles

    for article in created_articles:
        result = fx_app.delete(f'{ARTICLES_URL}/{article["id"]}', headers=fx_auth_admin)
        assert result.status_code == 204


@pytest.fixture
def fx_test_category(fx_app, fx_auth_admin) -> Generator[Any, None, None]:
    category_ids = []

    def _create_category(content_type: str) -> dict:
        new_category_data = {
            "name": f"fx_test_category_name_{time.time()}",
            "content_type": content_type,
        }

        new_category = fx_app.post(
            DIRECTORIES_CATEGORIES_URL, headers=fx_auth_admin, json=new_category_data
        )
        assert new_category.status_code == 201
        category = new_category.json
        category_ids.append(category["id"])
        return category

    yield _create_category

    for id_ in category_ids:
        deleted_category = fx_app.delete(
            f"{DIRECTORIES_CATEGORIES_URL}/{id_}", headers=fx_auth_admin
        )
        assert deleted_category.status_code == 204


@pytest.fixture
def fx_test_feedback(fx_app, fx_auth_admin, fx_test_category) -> Generator[dict, None, None]:
    new_feedback_data = {
        "category_id": fx_test_category("feedbacks")["id"],
        "email": fake.email(),
        "mobile_phone": "71234567890",
        "title": fake.sentence(),
        "message": fake.text(max_nb_chars=250),
    }
    new_feedback = fx_app.post(FEEDBACKS_URL, headers=fx_auth_admin, json=new_feedback_data)
    assert new_feedback.status_code == 201

    yield new_feedback.json

    deleted_feedback = fx_app.delete(
        f'{FEEDBACKS_URL}/{new_feedback.json["id"]}', headers=fx_auth_admin
    )
    assert deleted_feedback.status_code == 204


@pytest.fixture
def fx_test_user(fx_app, fx_auth_admin) -> Generator[dict, None, None]:
    new_user_data = {"username": fake.profile()["username"], "password": fake.password()}

    headers = {
        "Authorization": "Basic {}".format(
            base64.b64encode(
                f'{new_user_data["username"]}:{new_user_data["password"]}'.encode()
            ).decode()
        )
    }

    new_user = fx_app.post("/v1/signup", json=new_user_data)
    assert new_user.status_code == 201

    tokens = fx_app.post("/v1/login", headers=headers)
    assert tokens.status_code == 201

    yield new_user.json, headers, tokens.json, new_user_data

    deleted_user = fx_app.delete(f'{USERS_URL}/{new_user.json["id"]}', headers=fx_auth_admin)
    assert deleted_user.status_code == 204
