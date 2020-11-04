from typing import Tuple

import connexion

from nucleus.common.decorators import role_admin_required
from nucleus.controllers.clients import Client


@role_admin_required
def get_clients_list() -> dict:
    return Client.clients_list(connexion.request.args)


@role_admin_required
def create_client() -> Tuple:
    return Client.create(connexion.request.json).to_dict(), 201


@role_admin_required
def get_client(id) -> dict:
    return Client.get(id).to_dict()


@role_admin_required
def update_client(id) -> dict:
    return Client.update(id, connexion.request.json).to_dict()


@role_admin_required
def delete_client(id) -> Tuple:
    return Client.delete(id), 204
