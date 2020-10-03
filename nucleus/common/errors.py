from typing import Any
from typing import Tuple

from flask import current_app
from flask import Flask
from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from nucleus.models import db


def error_msg(exc: Any) -> None:
    """Make response for error and create log message."""
    current_app.logger.exception(
        f"{exc.__class__.__name__} "
        f"| request: {request.method} - {request.url} - {request.args} - {request.data} "
        f"| {exc}"
    )


def register_errors(app: Flask) -> Flask:
    """Registering handlers for common errors."""

    @app.errorhandler(NoResultFound)
    def obj_non_exist_in_db_exception(exc):
        """Exception for non exist object in db."""
        return {"code": 404, "name": "Not Found", "description": "Object not found."}, 404

    @app.errorhandler(IntegrityError)
    def unique_obj_exist_in_db_exception(exc):
        """Exception for exist unique object in db."""
        db.session.rollback()
        return {"code": 422, "name": "Unprocessable Entity", "description": "Object exists."}, 422

    @app.errorhandler(SQLAlchemyError)
    def database_exception(exc) -> Tuple:
        """Exception for all database errors."""
        error_msg(exc)
        return (
            {"code": 500, "name": "InternalDatabaseError", "description": "Common database error."},
            500,
        )

    @app.errorhandler(Exception)
    def common_exception(exc) -> Tuple:
        """Common exception for all errors."""
        error_msg(exc)
        return (
            {"code": 500, "name": "InternalServerError", "description": "Common server error."},
            500,
        )

    return app
