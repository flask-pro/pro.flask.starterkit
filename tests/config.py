from nucleus.config import Config


class TestConfig(Config):
    """Test environment config."""
    ENV = 'testing'
    DEBUG = 1
