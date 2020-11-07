import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Staging environment config."""

    BASE_DIR = basedir

    ENV = os.getenv("FLASK_ENV") or "development"
    DEBUG = os.getenv("FLASK_DEBUG") or 0
    JSON_AS_ASCII = False

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
    JWT_SECRET = os.environ["JWT_SECRET"]
    JWT_ACCESS_TOKEN_LIFETIME = 60 * 60
    JWT_REFRESH_TOKEN_LIFETIME = 30 * 24 * 60 * 60
    JWT_ALGORITHM = "HS256"

    # Files.
    FILES_BASE_DIR = os.path.join(BASE_DIR, "files")
    MAX_CONTENT_LENGTH = 128 * 1024 * 1024
    ALLOWED_EXTENSIONS = {
        "txt",
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "gif",
        "svg",
        "doc",
        "docx",
        "xls",
        "xlsx",
    }

    EXTENSIONS_FOR_THUMBNAILS = {"jpg", "jpeg", "png"}
    DEFAULT_THUMBNAIL = os.path.join(BASE_DIR, "content", "floppy.jpg")
    THUMBNAIL_SIZE_PX = 200, 200

    # ElasticSearch.
    ELASTICSEARCH_URL = os.environ["ELASTICSEARCH_URL"]
