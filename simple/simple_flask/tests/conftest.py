import sys
import os
sys.path.append(os.path.join(sys.path[0], '../../'))

from simple_flask.main import app
import pytest

@pytest.yield_fixture()
def init_app():
    # Init app for testing.
    app_context = app.app_context()
    app_context.push()

    yield app

    # Stop app for testing.
    app_context.pop()
