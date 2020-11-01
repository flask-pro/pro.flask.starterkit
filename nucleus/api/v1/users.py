from typing import Tuple

import connexion

from nucleus.common.decorators import role_admin_or_user_required
from nucleus.common.decorators import role_admin_required
from nucleus.controllers.users import Role
from nucleus.controllers.users import User


@role_admin_required
def get_users_list() -> dict:
    return User.users_list(connexion.request.args)


@role_admin_required
def create_user() -> Tuple:
    return User.create(connexion.request.json).to_dict(), 201


@role_admin_or_user_required
def get_user(id) -> dict:
    return User.get(id).to_dict()


@role_admin_or_user_required
def update_user(id) -> dict:
    return User.update(id, connexion.request.json).to_dict()


@role_admin_required
def delete_user(id) -> Tuple:
    return User.delete(id), 204


@role_admin_required
def get_roles_list() -> dict:
    return Role.roles_list(connexion.request.args)


@role_admin_required
def create_role() -> Tuple:
    return Role.create(connexion.request.json).to_dict(), 201


@role_admin_required
def get_role(id) -> dict:
    return Role.get(id).to_dict()


@role_admin_required
def update_role(id) -> dict:
    return Role.update(id, connexion.request.json).to_dict()


@role_admin_required
def delete_role(id) -> Tuple:
    return Role.delete(id), 204
