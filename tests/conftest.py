import base64
import os

import docker
import pytest
from docker import DockerClient
from docker.models.containers import Container
from flask import Flask

from .config import TestConfig
from nucleus import create_app

tests_basedir = os.path.abspath(os.path.dirname(__file__))


def _stop_database_container(docker_client: DockerClient, container_name: str) -> Container:
    db_container = docker_client.containers.get(container_name)
    db_container.stop()
    db_container.remove()
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
def fx_app() -> Flask:
    print("\n-> fx_app")

    # Return a docker client.
    docker_client = docker.client.from_env()

    _run_database_container(docker_client, TestConfig.PG_CONTAINER_NAME)

    # Init app for testing.
    app = create_app(TestConfig)
    app_context = app.app.app_context()
    app_context.push()

    with app.app.test_client() as test_client:
        yield test_client

    # Stop app for testing.
    app_context.pop()

    _run_database_container(docker_client, TestConfig.PG_CONTAINER_NAME)

    print("-> Teardown fx_app.")


@pytest.fixture()
def fx_auth_admin(fx_app) -> dict:
    print("\n-> fx_auth_admin")
    user = {"username": "admin", "password": "secret", "role": "admin"}
    headers = {
        "Authorization": "Basic {}".format(
            base64.b64encode(f'{user["username"]}:{user["password"]}'.encode()).decode()
        )
    }
    r = fx_app.post("/v1/login", headers=headers)
    assert r.status_code == 201

    yield {"Authorization": f'Bearer {r.json["access_token"]}'}
