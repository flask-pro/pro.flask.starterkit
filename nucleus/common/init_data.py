from flask import current_app
from sqlalchemy.exc import IntegrityError

from nucleus.common.extensions import db
from nucleus.common.fake_data.load_data import load_fake_data
from nucleus.config import Config
from nucleus.controllers.users import role_controller
from nucleus.controllers.users import user_controller

ENV = Config.ENV

roles = [
    {"name": "admin", "description": "Administration user"},
    {"name": "user", "description": "Regular user"},
]

users = [{"email": "admin@nucleus.admin", "password": "secret", "role": "admin"}]


def _load_roles(roles: list) -> None:
    for role in roles:
        try:
            role_controller.create(role)
        except IntegrityError:
            db.session.rollback()
            current_app.logger.warning(f"Load init data | error load role | {role}")
            continue


def _load_users(users: list) -> None:
    for user in users:
        try:
            user_controller.create(user)
        except IntegrityError:
            db.session.rollback()
            current_app.logger.warning(f"Load init data | error load user | {user}")
            continue


def load_init_data() -> None:
    """Load initial data when the application starts."""
    _load_roles(roles)
    _load_users(users)
    if ENV not in ["production"]:
        load_fake_data()
