import os
from contextlib import suppress

from flask import abort
from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from nucleus.config import Config
from nucleus.controllers.base import BaseController
from nucleus.models.files import Files as FilesModel

FILES_BASE_DIR = Config.FILES_BASE_DIR
THUMBNAIL_SIZE_PX = Config.THUMBNAIL_SIZE_PX
ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS
EXTENSIONS_FOR_THUMBNAILS = Config.EXTENSIONS_FOR_THUMBNAILS


class File(BaseController):
    """Management of the user."""

    @staticmethod
    def _is_allow_extension(filename, extensions):
        """Check file containse allowed extension."""
        return "." in filename and filename.rsplit(".", 1)[1].lower() in extensions

    @classmethod
    def create_thumbnail(cls, file: FileStorage, parent_filename: str):
        im = Image.open(file)
        im.thumbnail(THUMBNAIL_SIZE_PX)
        thumbnail_path = os.path.join(FILES_BASE_DIR, "thumbnails", parent_filename)
        im.save(thumbnail_path, "png")

    def create(self, file: FileStorage) -> FilesModel:
        if not file:
            abort(422, "No file part")

        # if user does not select file, browser also submit an empty part without filename
        elif file.filename == "":
            abort(422, "No selected file")

        elif file and self._is_allow_extension(file.filename, ALLOWED_EXTENSIONS):

            filename = secure_filename(os.path.basename(file.filename))

            new_file = {"name": filename, "mime_type": file.mimetype}

            created_file = self.model_manager.create(new_file)
            file.save(os.path.join(FILES_BASE_DIR, created_file.id))

            # Get file length.
            file.seek(0, os.SEEK_END)
            file_length = file.tell()

            created_file = self.model_manager.patch(created_file.id, {"length": file_length})

            if self._is_allow_extension(file.filename, EXTENSIONS_FOR_THUMBNAILS):
                self.create_thumbnail(file, created_file.id)

            return created_file
        else:
            abort(422, "File not allowed.")

    def delete(self, id_: str) -> None:
        file = self.model_manager.delete(id_)
        file_path = os.path.join(FILES_BASE_DIR, file.id)
        os.remove(file_path)
        with suppress(FileNotFoundError):
            os.remove(os.path.join(FILES_BASE_DIR, "thumbnails", file.id))


file_controller = File(FilesModel)
