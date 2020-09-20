import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, "..", ".env"))


class Config:
    """Staging environment config."""

    BASE_DIR = basedir

    ENV = "development"
    DEBUG = os.getenv("FLASK_DEBUG") or 0

    # Database settings.
    PG_DB = os.environ["POSTGRES_DB"]
    PG_USER = os.environ["POSTGRES_USER"]
    PG_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    PG_HOST = os.environ["POSTGRES_HOST"]
    PG_PORT = os.environ["POSTGRES_PORT"]
    SQLALCHEMY_DATABASE_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pagination.
    ITEMS_PER_PAGE = 30
    MAX_PER_PAGE = 100

    # Authorization.
    JWT_ISSUER = "pro.flask.starterkit"
    JWT_SECRET = "obTVtYBgPXqeFSW47S1WLOY5MFLJrdE5Ip7j8387qywfgtfGUIhAG8SaR89mCYm5xt2mCwIrF8BgQUtSa"
    JWT_ACCESS_TOKEN_LIFETIME = 60 * 60
    JWT_REFRESH_TOKEN_LIFETIME = 30 * 24 * 60 * 60
    JWT_ALGORITHM = "HS256"
