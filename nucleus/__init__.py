import time
from logging.config import dictConfig
from typing import Type

import connexion
from sqlalchemy.exc import SQLAlchemyError

from nucleus.common.errors import register_errors
from nucleus.common.logging import logging_configuration
from nucleus.config import Config
from nucleus.models import db
from nucleus.views.services import registration_service_routes
from nucleus.common.load_data import load_init_data


def create_app(config_app: Type[Config]):
    """Application factory."""

    # Logging.
    dictConfig(logging_configuration)

    # Init application.
    options = {'swagger_url': '/docs'}
    app_conn = connexion.FlaskApp(__name__, specification_dir='openapi/', options=options)
    app_conn.add_api('nucleus.yaml', base_path='/v1', validate_responses=True)

    # Flask app.
    app = app_conn.app
    app.config.from_object(config_app)

    # Flask extensions.
    db.init_app(app)

    # Registration routes.
    registration_service_routes(app)

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
        load_init_data()
        app.logger.info('Database created!')

    return app_conn
