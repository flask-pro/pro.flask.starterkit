import os

from nucleus.config import Config

basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig(Config):
    """Test environment config."""

    BASE_DIR = basedir

    ENV = "testing"
    DEBUG = 1

    # API routes.
    FILES_URL = "/v1/files"
    ROLES_URL = "/v1/roles"
    USERS_URL = "/v1/users"
    CLIENTS_URL = "/v1/clients"
    SEARCH_URL = "/v1/search"
    PROFILES_URL = "/v1/profiles"

    # Blueprints routes.
    MAIN_URL = "/"
