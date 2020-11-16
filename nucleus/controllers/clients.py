from flask import abort
from flask import current_app

from nucleus.controllers.utils import Items
from nucleus.controllers.utils import ModelManager
from nucleus.models.clients import Clients as ClientsModel


class Client:
    """Management of the client."""

    TABLE_MODEL = ModelManager(ClientsModel)

    @staticmethod
    def get_clients_list(parameters: dict) -> dict:
        ITEMS_PER_PAGE = current_app.config["ITEMS_PER_PAGE"]
        MAX_PER_PAGE = current_app.config["MAX_PER_PAGE"]

        clients_list = Items(
            model=ClientsModel, include_metadata=parameters.get("include_metadata", False)
        )
        clients_list.ITEMS_PER_PAGE = ITEMS_PER_PAGE
        clients_list.MAX_PER_PAGE = MAX_PER_PAGE
        clients_list = clients_list.result(
            int(parameters.get("page", 1)), int(parameters.get("per_page", ITEMS_PER_PAGE))
        )

        return clients_list

    @classmethod
    def create(cls, client: dict) -> ClientsModel:
        return cls.TABLE_MODEL.create(client)

    @classmethod
    def get(cls, id_: str) -> ClientsModel:
        return cls.TABLE_MODEL.get(id_)

    @classmethod
    def update(cls, id_: str, client: dict) -> ClientsModel:
        if id_ != client.get("id"):
            abort(400, "ID is required!")
        return cls.TABLE_MODEL.update(id_, client)

    @classmethod
    def delete(cls, id_: str) -> dict:
        if cls.TABLE_MODEL.delete(id_):
            return ""
        else:
            abort(404, "Object not found!")
