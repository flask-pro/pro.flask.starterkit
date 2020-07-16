import time
from logging.config import dictConfig
from typing import Type

from flask import Flask
from sqlalchemy.exc import SQLAlchemyError

from nucleus.common.errors import register_errors
from nucleus.common.logging import logging_configuration
from nucleus.config import Config
from nucleus.models import db
from nucleus.views.services import registration_service_routes
from nucleus.views.users import registration_user_routes


def create_app(config_app: Type[Config]):
    """Application factory."""

    # Logging.
    dictConfig(logging_configuration)

    # Init application.
    app = Flask(__name__)
    app.config.from_object(config_app)

    # Подключение расширений Flask.
    # Flask-SQLAlchemy.
    db.init_app(app)

    # Registration routes.
    registration_service_routes(app)
    registration_user_routes(app)

    # Registration handlers.
    register_errors(app)

    # Create tables in database.
    with app.app_context():
        for i in range(10):
            try:
                db.engine.execute('SELECT version();')
                break
            except SQLAlchemyError as err:
                app.logger.warning(f'Database not available: {err}!')
                time.sleep(1)

        db.create_all()
        app.logger.info('Database created!')

    return app
