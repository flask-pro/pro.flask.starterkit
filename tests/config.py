import os

from nucleus.config import Config

basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig(Config):
    """Test environment config."""

    BASE_DIR = basedir

    TESTING = True
    DEBUG = 1

    # API routes.
    FILES_URL = "/v1/files"
    ROLES_URL = "/v1/roles"
    USERS_URL = "/v1/users"
    SEARCH_URL = "/v1/search"
    PROFILES_URL = "/v1/profiles"
    ACCOUNTS_URL = "/v1/accounts"
    DIRECTORIES_URL = "/v1/directories"
    DIRECTORIES_CATEGORIES_URL = "/v1/directories/categories"
    ARTICLES_URL = "/v1/articles"
    FEEDBACKS_URL = "/v1/feedbacks"
    LOGS_URL = "/v1/logs"

    # Blueprints routes.
    MAIN_URL = "/"
