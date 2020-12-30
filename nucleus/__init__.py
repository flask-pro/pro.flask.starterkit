import os
import sys
import time
from logging.config import dictConfig
from typing import Type

import connexion
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
from sqlalchemy.exc import SQLAlchemyError

from nucleus.common.contexts import register_context_handlers
from nucleus.common.errors import register_errors
from nucleus.common.extensions import db
from nucleus.common.extensions import register_extensions
from nucleus.common.init_data import load_init_data
from nucleus.common.logging import logging_configuration
from nucleus.config import Config


def create_app(config_app: Type[Config]) -> connexion:
    """Application factory."""

    # Logging.
    dictConfig(logging_configuration)

    # Init application.
    options = {"swagger_url": "/docs"}
    app_conn = connexion.App(__name__, specification_dir="openapi/", options=options)
    app_conn.add_api("nucleus.yaml", base_path="/v1", validate_responses=True)

    # Flask app.
    app = app_conn.app
    app.config.from_object(config_app)

    # Flask extensions.
    register_extensions(app)

    # Registration routes.
    from nucleus.views.services import services

    app.register_blueprint(services)

    # Registration error handlers.
    register_errors(app)

    # Registration context handlers
    register_context_handlers(app)

    # Wait run Elasticsearch.
    with app.app_context():
        elasticsearch = Elasticsearch([app.config["ELASTICSEARCH_URL"]])
        for _ in range(15):
            try:
                elasticsearch.info()
                break
            except ConnectionError as err:
                app.logger.warning(f"Elasticsearch not available: {err}!")
                time.sleep(1)
        try:
            elasticsearch.info()
            app.logger.info("Elasticsearch available!")
        except ConnectionError as err:
            app.logger.warning(f"Elasticsearch not available: {err}!")
            sys.exit()

    # Create folder for files.
    for _ in range(3):
        try:
            os.makedirs(os.path.join(app.config["FILES_BASE_DIR"], "thumbnails"))
            app.logger.info("Folder for files created!")
            break
        except FileExistsError:
            app.logger.info("Folder for files exist!")
            break
        except Exception as err:
            app.logger.warning(f"Folder for files not available: {err}!")
            sys.exit()

    # Create tables in database.
    with app.app_context():
        for _ in range(10):
            try:
                db.engine.execute("SELECT version();")
                break
            except SQLAlchemyError as err:
                app.logger.warning(f"Database not available: {err}!")
                time.sleep(1)
        try:
            db.create_all()
            load_init_data()
            app.logger.info("Database created!")

            # UWSGI создаёт форки процесса, что вызывает использование одного и того же пула
            # соединений с БД всеми форками. "db.engine.dispose()" закрывает пул, в результате
            # происходит пересоздание пула для каждого форка.
            # Детали - https://docs.sqlalchemy.org/en/13/core/connections.html#engine-disposal
            db.session.remove()
            db.engine.dispose()

        except SQLAlchemyError as err:
            app.logger.warning(f"Database not created: {err}!")
            sys.exit()

    return app_conn
