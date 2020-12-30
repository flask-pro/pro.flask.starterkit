import os
from contextlib import suppress

from nucleus.common.extensions import db
from nucleus.common.search import FulltextSearch
from nucleus.config import Config
from nucleus.controllers.utils import Items
from nucleus.controllers.utils import ModelManager
from nucleus.models.files import Files as FilesModels

ITEMS_PER_PAGE = Config.ITEMS_PER_PAGE
MAX_PER_PAGE = Config.MAX_PER_PAGE

FILES_BASE_DIR = Config.FILES_BASE_DIR


class BaseController:
    def __init__(self, model: db.Model):
        self.model = model
        self.model_manager = ModelManager(self.model)

    def _file_delete(self, id_: str) -> FilesModels:
        file = FilesModels.query.filter_by(id=id_).one()
        db.session.delete(file)
        db.session.commit()

        file_path = os.path.join(FILES_BASE_DIR, file.id)
        os.remove(file_path)
        with suppress(FileNotFoundError):
            os.remove(os.path.join(FILES_BASE_DIR, "thumbnails", file.id))

        return file

    def get_list(self, parameters: dict, announce: bool = False) -> dict:

        obj_list = Items(
            model=self.model, include_metadata=parameters.get("include_metadata", False)
        )
        obj_list.ITEMS_PER_PAGE = ITEMS_PER_PAGE
        obj_list.MAX_PER_PAGE = MAX_PER_PAGE
        result = obj_list.result(parameters, announce=announce)

        return result

    def create(self, params: dict) -> db.Model:
        obj = self.model_manager.create(params)
        FulltextSearch.add_to_index(obj)
        return obj

    def get(self, id_: str) -> db.Model:
        return self.model_manager.get(id_)

    def update(self, parameters: dict) -> db.Model:
        old_obj = self.get(parameters["id"])
        old_files = {field: getattr(old_obj, field) for field in self.model.__files__}

        updated_obj = self.model_manager.update(parameters)

        # Файлы создаются независимо от сущностей к которым они привязываются.
        # При замене привязки требуется удалять отвязанные файлы.
        for key, value in parameters.items():
            if key in old_files and value != old_files[key]:
                self._file_delete(old_files[key])

        FulltextSearch.add_to_index(updated_obj)

        return updated_obj

    def delete(self, id_: str) -> db.Model:
        if self.model.__name__ != "Files":
            deleted_obj = self.model_manager.delete(id_)

            for file_field in self.model.__files__:
                file_id = getattr(deleted_obj, file_field)
                if file_id:
                    self._file_delete(file_id)
        else:
            deleted_obj = self._file_delete(id_)

        FulltextSearch.remove_from_index(deleted_obj)

        return deleted_obj
