import traceback
from datetime import datetime
from typing import Any
from typing import Tuple

from flask import current_app
from flask import Flask
from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from nucleus.common.extensions import db
from nucleus.common.telegram import send_to_telegram
from nucleus.config import Config


def error_msg(exc: Any, exc_info: bool = False) -> None:
    """Create log message."""
    current_app.logger.error(
        "%s | request: %s - %s - %s - %s | %s",
        exc.__class__.__name__,
        request.method,
        request.url,
        request.args,
        request.data,
        repr(exc),
        exc_info=exc_info,
    )


def exception_error_msg(exc: Any) -> None:
    """Send error to telegram."""

    header = f"Attention! Instance <{Config.ENV}> | {datetime.now()}"
    request_params = (
        f"Request:\n"
        f"    Method: {request.method}\n"
        f"    URL: {request.url}\n"
        f"    Headers: {dict(request.headers)}\n"
        f"    Arguments: {dict(request.args)}\n"
        f"    Data: {request.data}"
    )
    trace = f"Traceback (most recent call last):\n{''.join(traceback.format_tb(exc.__traceback__))}"
    message = f"{header}\n\n{request_params}\n\n{trace}"

    send_to_telegram(message)

    error_msg(exc, exc_info=True)


class NoResultSearch(Exception):
    """Exception if search non result."""


def register_errors(app: Flask) -> Flask:
    """Registering handlers for common errors."""

    @app.errorhandler(NoResultSearch)
    def search_non_result_exception(exc) -> Tuple:
        """Exception if search non result."""
        error_msg(exc)
        return (
            {
                "code": 404,
                "name": "Not Found",
                "description": "The search did not return any results.",
            },
            404,
        )

    @app.errorhandler(NoResultFound)
    def obj_non_exist_in_db_exception(exc) -> Tuple:
        """Exception for non exist object in db."""
        error_msg(exc)
        return {"code": 404, "name": "Not Found", "description": "Object not found."}, 404

    @app.errorhandler(IntegrityError)
    def unique_obj_exist_in_db_exception(exc):
        """Exception for exist unique object in db."""
        error_msg(exc)
        db.session.rollback()
        return {"code": 422, "name": "Unprocessable Entity", "description": "Object exists."}, 422

    @app.errorhandler(SQLAlchemyError)
    def database_exception(exc) -> Tuple:
        """Exception for all database errors."""
        exception_error_msg(exc)
        return (
            {"code": 500, "name": "InternalDatabaseError", "description": "Common database error."},
            500,
        )

    @app.errorhandler(Exception)
    def common_exception(exc) -> Tuple:
        """Common exception for all errors."""
        exception_error_msg(exc)
        return (
            {"code": 500, "name": "InternalServerError", "description": "Common server error."},
            500,
        )

    return app
