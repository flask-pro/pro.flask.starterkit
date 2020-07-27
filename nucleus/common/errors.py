from typing import Any

from flask import Flask, current_app, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound


def error_msg(exc: Any):
    """Make response for error and create log message."""
    current_app.logger.exception(
        f'{exc.__class__.__name__} '
        f'| request: {request.host} - {request.method} - {request.url} - {request.args} - {request.data} '
        f'| {exc}'
    )


def register_errors(app: Flask):
    """Registering handlers for common errors."""

    @app.errorhandler(NoResultFound)
    def database_exception(exc):
        """Exception for non exist object in db."""
        return {'code': 404, 'name': 'Not Found',
                'description': 'Object not found.'}, 404

    @app.errorhandler(SQLAlchemyError)
    def database_exception(exc):
        """Exception for all database errors."""
        error_msg(exc)
        return {'code': 500, 'name': 'InternalDatabaseError',
                'description': 'Common database error.'}, 500

    @app.errorhandler(Exception)
    def common_exception(exc):
        """Common exception for all errors."""
        error_msg(exc)
        return {'code': 500, 'name': 'InternalServerError',
                'description': 'Common server error.'}, 500
