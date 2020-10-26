import base64
import os
from typing import Generator

import docker
import pytest
from docker import DockerClient
from docker.models.containers import Container
from flask.testing import FlaskClient

from nucleus import create_app
from tests.config import TestConfig

BASE_DIR = TestConfig.BASE_DIR
FILES_URL = TestConfig.FILES_URL


def _stop_database_container(docker_client: DockerClient, container_name: str) -> Container:
    db_container = docker_client.containers.get(container_name)
    db_container.stop()
    db_container.remove(v=True)
    return db_container


def _run_database_container(docker_client: DockerClient, container_name: str) -> Container:
    try:
        _stop_database_container(docker_client, container_name)
    except docker.errors.NotFound:
        pass

    new_db_container = docker_client.containers.run(
        image=TestConfig.PG_IMAGE,
        name=container_name,
        environment={
            "POSTGRES_DB": TestConfig.PG_DB,
            "POSTGRES_USER": TestConfig.PG_USER,
            "POSTGRES_PASSWORD": TestConfig.PG_PASSWORD,
            "POSTGRES_HOST": TestConfig.PG_HOST,
            "POSTGRES_PORT": TestConfig.PG_PORT,
        },
        ports={5432: TestConfig.PG_PORT},
        detach=True,
    )
    return new_db_container


@pytest.fixture(scope="session")
def fx_docker() -> DockerClient:
    """Returns a client object for accessing docker.

    :return: docker client object
    """
    print("\n-> fx_docker")
    return docker.client.from_env()


@pytest.fixture(scope="session")
def fx_app(fx_docker) -> Generator[FlaskClient, None, None]:
    """Returns a flask object for accessing application.

    :return: flask test client object
    """
    print("\n-> fx_app")

    _run_database_container(fx_docker, TestConfig.PG_CONTAINER_NAME)

    # Init app for testing.
    app = create_app(TestConfig)
    app_context = app.app.app_context()
    app_context.push()

    with app.app.test_client() as test_client:
        yield test_client

    # Stop app for testing.
    app_context.pop()

    _stop_database_container(fx_docker, TestConfig.PG_CONTAINER_NAME)

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
