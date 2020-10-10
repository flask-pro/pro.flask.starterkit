import os

from nucleus.config import Config

basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig(Config):
    """Test environment config."""

    BASE_DIR = basedir

    ENV = "testing"
    DEBUG = 1

    PG_IMAGE = "postgres:13-alpine"
    PG_CONTAINER_NAME = "test_db_container"
    PG_HOST = "localhost"
    PG_DB = "test_db"
    PG_USER = "postgres"
    PG_PASSWORD = "super_secret"
    PG_PORT = 54321
    SQLALCHEMY_DATABASE_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

    # Files.
    FILES_BASE_DIR = os.path.join(BASE_DIR, "files")

    # Routes.
    FILES_URL = "/v1/files"
    ROLES_URL = "/v1/roles"
    USERS_URL = "/v1/users"
