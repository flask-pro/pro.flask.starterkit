from typing import Tuple

import connexion

from nucleus.api.v1.utils import check_to_equality
from nucleus.common.decorators import role_admin_or_user_required
from nucleus.common.decorators import role_admin_required
from nucleus.controllers.users import role_controller
from nucleus.controllers.users import user_controller


@role_admin_required
def get_users_list() -> dict:
    return user_controller.get_list(connexion.request.args)


@role_admin_required
def create_user() -> Tuple:
    return user_controller.create(connexion.request.json).to_dict(), 201


@role_admin_or_user_required
def get_user(id) -> dict:
    return user_controller.get(id).to_dict()


@role_admin_or_user_required
def update_user(id) -> dict:
    parameters = connexion.request.json
    check_to_equality(id, "id", parameters)
    return user_controller.update(parameters).to_dict()


@role_admin_required
def delete_user(id) -> Tuple:
    user_controller.delete(id)
    return None, 204


@role_admin_required
def block_user(id) -> dict:
    return user_controller.block(id).to_dict()


@role_admin_required
def unblock_user(id) -> dict:
    return user_controller.unblock(id).to_dict()


@role_admin_required
def get_roles_list() -> dict:
    return role_controller.get_list(connexion.request.args)


@role_admin_required
def create_role() -> Tuple:
    return role_controller.create(connexion.request.json).to_dict(), 201


@role_admin_required
def get_role(id) -> dict:
    return role_controller.get(id).to_dict()


@role_admin_required
def update_role(id) -> dict:
    parameters = connexion.request.json
    check_to_equality(id, "id", parameters)
    return role_controller.update(parameters).to_dict()


@role_admin_required
def delete_role(id) -> Tuple:
    role_controller.delete(id)
    return None, 204
