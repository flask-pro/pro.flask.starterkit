import os

from flask import abort
from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from nucleus.controllers.utils import Items
from nucleus.controllers.utils import ModelManager
from nucleus.models.files import Files


class File:
    """Management of the user."""

    TABLE_MODEL = ModelManager(Files)

    @staticmethod
    def _allowed_file(filename: str) -> bool:
        """Check file containse allowed extension."""
        ALLOWED_EXTENSIONS = current_app.config["ALLOWED_EXTENSIONS"]
        return all(["." in filename, filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS])

    @staticmethod
    def file_list(parameters: dict) -> dict:
        ITEMS_PER_PAGE = current_app.config["ITEMS_PER_PAGE"]
        MAX_PER_PAGE = current_app.config["MAX_PER_PAGE"]

        users_list = Items(model=Files, include_metadata=parameters.get("include_metadata", False))
        users_list.ITEMS_PER_PAGE = ITEMS_PER_PAGE
        users_list.MAX_PER_PAGE = MAX_PER_PAGE
        users_list = users_list.result(
            int(parameters.get("page", 1)), int(parameters.get("per_page", ITEMS_PER_PAGE))
        )

        return users_list

    @classmethod
    def create(cls, file: FileStorage) -> dict:
        if not file:
            abort(422, "No file part")

        # if user does not select file, browser also submit an empty part without filename
        if file.filename == "":
            abort(422, "No selected file")

        if not cls._allowed_file(file.filename):
            abort(422, "File not allowed.")

        filename = secure_filename(os.path.basename(file.filename))

        new_file = {"name": filename, "mime_type": file.mimetype}

        file_from_db = cls.TABLE_MODEL.create(new_file)

        file.save(os.path.join(current_app.config["FILES_BASE_DIR"], str(file_from_db.id)))

        # Get file length.
        file_length = os.path.getsize(
            os.path.join(current_app.config["FILES_BASE_DIR"], str(file_from_db.id))
        )

        return cls.TABLE_MODEL.patch(str(file_from_db.id), {"length": file_length}).to_dict()

    @classmethod
    def get(cls, id_: str) -> dict:
        return cls.TABLE_MODEL.get(id_).to_dict()

    @classmethod
    def delete(cls, id_: str) -> [str, dict]:
        file = cls.TABLE_MODEL.get(id_)
        if cls.TABLE_MODEL.delete(file.id):
            os.remove(os.path.join(current_app.config["FILES_BASE_DIR"], str(file.id)))
            return ""
        else:
            abort(404, "Object not found!")
