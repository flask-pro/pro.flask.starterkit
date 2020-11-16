import os
from contextlib import suppress

from flask import abort
from flask import current_app
from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from nucleus.config import Config
from nucleus.controllers.utils import Items
from nucleus.controllers.utils import ModelManager
from nucleus.models.files import Files

FILES_BASE_DIR = Config.FILES_BASE_DIR
THUMBNAIL_SIZE_PX = Config.THUMBNAIL_SIZE_PX
ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS
EXTENSIONS_FOR_THUMBNAILS = Config.EXTENSIONS_FOR_THUMBNAILS


class File:
    """Management of the user."""

    TABLE_MODEL = ModelManager(Files)

    @staticmethod
    def _is_allow_extension(filename, extensions):
        """Check file containse allowed extension."""
        return "." in filename and filename.rsplit(".", 1)[1].lower() in extensions

    @staticmethod
    def get_files_list(parameters: dict) -> dict:
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
    def create_thumbnail(cls, file: FileStorage, parent_filename: str):
        im = Image.open(file)
        im.thumbnail(THUMBNAIL_SIZE_PX)
        thumbnail_path = os.path.join(FILES_BASE_DIR, "thumbnails", str(parent_filename))
        im.save(thumbnail_path, "png")

    @classmethod
    def create(cls, file: FileStorage) -> dict:
        if not file:
            abort(422, "No file part")

        # if user does not select file, browser also submit an empty part without filename
        elif file.filename == "":
            abort(422, "No selected file")

        elif file and cls._is_allow_extension(file.filename, ALLOWED_EXTENSIONS):

            filename = secure_filename(os.path.basename(file.filename))

            new_file = {"name": filename, "mime_type": file.mimetype}

            created_file = cls.TABLE_MODEL.create(new_file)
            file.save(os.path.join(FILES_BASE_DIR, str(created_file.id)))

            # Get file length.
            file.seek(0, os.SEEK_END)
            file_length = file.tell()

            created_file = cls.TABLE_MODEL.patch(created_file.id, {"length": file_length}).to_dict()

            if cls._is_allow_extension(file.filename, EXTENSIONS_FOR_THUMBNAILS):
                cls.create_thumbnail(file, created_file["id"])

            return created_file
        else:
            abort(422, "File not allowed.")

    @classmethod
    def get(cls, id_: str) -> dict:
        return cls.TABLE_MODEL.get(id_).to_dict()

    @classmethod
    def delete(cls, id_: str) -> dict:
        file = cls.TABLE_MODEL.get(id_)
        file_path = os.path.join(FILES_BASE_DIR, str(file.id))
        if cls.TABLE_MODEL.delete(file.id):
            os.remove(file_path)
            with suppress(FileNotFoundError):
                os.remove(os.path.join(FILES_BASE_DIR, "thumbnails", str(file.id)))
            return ""
        else:
            abort(404, "Object not found!")
