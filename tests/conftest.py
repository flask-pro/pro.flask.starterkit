import base64
import os
import subprocess

import pytest

from nucleus import create_app
from .config import TestConfig

tests_basedir = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="session")
def fx_app():
    print('\n-> fx_app')

    # Run database container.
    subprocess.run(['make', f'--directory={tests_basedir}/..', 'test_start'],
                   stdout=subprocess.PIPE).stdout.decode('utf-8')

    # Init app for testing.
    app = create_app(TestConfig)
    app_context = app.app.app_context()
    app_context.push()

    with app.app.test_client() as test_client:
        yield test_client

    # Stop app for testing.
    app_context.pop()

    # Stop database container.
    subprocess.run(['make', f'--directory={tests_basedir}/..', 'test_end'],
                   stdout=subprocess.PIPE).stdout.decode('utf-8')

    print('-> Teardown fx_app.')


@pytest.fixture()
def fx_auth_admin(fx_app):
    print('\n-> fx_auth_admin')
    user = {'username': 'admin', 'password': 'secret', 'role': 'admin'}
    headers = {'Authorization': 'Basic {}'.format(
        base64.b64encode(f'{user["username"]}:{user["password"]}'.encode()).decode())}
    r = fx_app.post('/v1/login', headers=headers)
    assert r.status_code == 201

    yield {'Authorization': f'Bearer {r.json["access_token"]}'}
