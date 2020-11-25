from flask import current_app
from sqlalchemy.exc import IntegrityError

from nucleus.controllers.users import user_controller
from nucleus.models.users import Roles

roles = [
    {"name": "admin", "description": "Administration user"},
    {"name": "user", "description": "Regular user"},
]

user_admin = {"username": "admin", "password": "secret", "role": "admin"}


def load_init_data() -> bool:
    """Load initial data when the application starts."""
    try:
        Roles.bulk_create(roles)
        user_controller.create(user_admin)
    except IntegrityError as err:
        current_app.logger.info(f"Load init data | error load user | {repr(err)}")
    return True
