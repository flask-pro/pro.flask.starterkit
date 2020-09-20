from nucleus.config import Config


class TestConfig(Config):
    """Test environment config."""

    ENV = "testing"
    DEBUG = 1

    # Routes.
    ROLES_URL = "/v1/roles"
    USERS_URL = "/v1/users"
