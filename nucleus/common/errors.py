from typing import Any

from flask import Flask, current_app, request
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError


def error_msg(exc: Any):
    """Make response for error and create log message."""
    current_app.logger.exception(
        f'{exc.__class__.__name__} '
        f'| request: {request.host} - {request.method} - {request.url} - {request.args} - {request.data} '
        f'| {exc}'
    )


def register_errors(app: Flask):
    """Registering handlers for unexpected errors."""

    @app.errorhandler(SQLAlchemyError)
    def database_exception(exc):
        """Exception for all database errors."""

        error_msg(exc)

        return {'code': 500, 'name': 'InternalDatabaseError',
                'description': 'Common database error.'}, 500

    @app.errorhandler(InternalServerError)
    def common_exception(exc):
        """Common exception for all errors."""

        error_msg(exc)

        return {'code': 500, 'name': 'InternalServerError',
                'description': 'Common server error.'}, 500
