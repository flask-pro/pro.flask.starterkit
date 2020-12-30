from typing import Tuple

import connexion

from nucleus.api.v1.utils import check_to_equality
from nucleus.common.decorators import role_admin_required
from nucleus.controllers.directories import categories_controller
from nucleus.controllers.directories import Directory


def get_directories() -> dict:
    return Directory.get_directories()


@role_admin_required
def get_categories_list() -> dict:
    return categories_controller.get_list(connexion.request.args)


@role_admin_required
def create_category() -> Tuple:
    return categories_controller.create(connexion.request.json).to_dict(), 201


@role_admin_required
def get_category(id) -> dict:
    return categories_controller.get(id).to_dict()


@role_admin_required
def update_category(id) -> dict:
    parameters = connexion.request.json
    check_to_equality(id, "id", parameters)
    return categories_controller.update(parameters).to_dict()


@role_admin_required
def delete_category(id) -> Tuple:
    categories_controller.delete(id)
    return None, 204
