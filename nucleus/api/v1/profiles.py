from typing import Tuple

import connexion

from nucleus.common.decorators import role_admin_required
from nucleus.controllers.profiles import Profile


@role_admin_required
def get_profiles_list() -> dict:
    return Profile.get_profiles_list(connexion.request.args)


@role_admin_required
def create_profile() -> Tuple:
    return Profile.create(connexion.request.json).to_dict(), 201


@role_admin_required
def get_profile(id) -> dict:
    return Profile.get(id).to_dict()


@role_admin_required
def update_profile(id) -> dict:
    return Profile.update(id, connexion.request.json).to_dict()


@role_admin_required
def delete_profile(id) -> Tuple:
    return Profile.delete(id), 204
