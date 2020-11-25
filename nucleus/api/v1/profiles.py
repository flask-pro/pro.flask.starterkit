from typing import Tuple

import connexion

from nucleus.common.decorators import role_admin_required
from nucleus.controllers.profiles import profile_controller


@role_admin_required
def get_profiles_list() -> dict:
    return profile_controller.get_list(connexion.request.args)


@role_admin_required
def create_profile() -> Tuple:
    return profile_controller.create(connexion.request.json).to_dict(), 201


@role_admin_required
def get_profile(id) -> dict:
    return profile_controller.get(id).to_dict()


@role_admin_required
def update_profile(id) -> dict:
    return profile_controller.update(id, connexion.request.json).to_dict()


@role_admin_required
def delete_profile(id) -> Tuple:
    return profile_controller.delete(id), 204
