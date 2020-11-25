from flask import abort

from nucleus.common.extensions import db
from nucleus.common.search import FulltextSearch
from nucleus.config import Config
from nucleus.controllers.utils import Items
from nucleus.controllers.utils import ModelManager

ITEMS_PER_PAGE = Config.ITEMS_PER_PAGE
MAX_PER_PAGE = Config.MAX_PER_PAGE


class BaseController:
    def __init__(self, model: db.Model):
        self.model = model
        self.model_manager = ModelManager(self.model)

    def get_list(self, parameters: dict, announce: bool = False) -> dict:

        obj_list = Items(
            model=self.model, include_metadata=parameters.get("include_metadata", False)
        )
        obj_list.ITEMS_PER_PAGE = ITEMS_PER_PAGE
        obj_list.MAX_PER_PAGE = MAX_PER_PAGE
        obj_list = obj_list.result(parameters, announce)

        return obj_list

    def get_all_items(self) -> list:
        return [item.to_dict() for item in self.model_manager.get_all_items()]

    def create(self, params: dict) -> db.Model:
        obj = self.model_manager.create(params)
        FulltextSearch.add_to_index(obj)
        return obj

    def get(self, id_: str) -> db.Model:
        return self.model_manager.get(id_)

    def update(self, id_: str, params: dict) -> db.Model:
        if id_ != params.get("id"):
            abort(400, "ID is required!")

        old_obj = self.get(id_)
        old_files = {field: getattr(old_obj, field) for field in self.model.__files__}

        updated_obj = self.model_manager.update(id_, params)

        # Файлы создаются независимо от сущностей к которым они привязываются.
        # При замене привязки требуется удалять отвязанные файлы.
        for key, value in params.items():
            if key in old_files and value != old_files[key]:
                # Отложено на будущий рефакторинг.
                # Хороших идей нет, вероятно нужно перенести в класс потомок.
                from nucleus.controllers.files import file_controller

                file_controller.delete(old_files[key])

        FulltextSearch.add_to_index(updated_obj)

        return updated_obj

    def delete(self, id_: str) -> None:
        obj = self.model_manager.delete(id_)
        FulltextSearch.remove_from_index(obj)
