from typing import Tuple

import connexion
from flask import request

from nucleus.controllers.users import Role
from nucleus.controllers.users import User


def get_users_list() -> dict:
    return User.users_list(connexion.request.args)


def create_user() -> Tuple:
    return User.create(request.json), 201


def get_user(id) -> dict:
    return User.get(id)


def update_user(id) -> dict:
    return User.update(id, request.json)


def delete_user(id) -> Tuple:
    return User.delete(id), 204


def get_roles_list() -> dict:
    return Role.roles_list(connexion.request.args)


def create_role() -> Tuple:
    return Role.create(request.json), 201


def get_role(id) -> dict:
    return Role.get(id)


def update_role(id) -> dict:
    return Role.update(id, request.json)


def delete_role(id) -> Tuple:
    return Role.delete(id), 204
