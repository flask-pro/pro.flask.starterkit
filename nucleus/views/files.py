import os

import connexion
from flask import current_app
from flask import send_file

from nucleus.controllers.files import File


def file_list():
    return File.file_list(connexion.request.args)


def upload_file():
    return File.create(connexion.request.files.get("file")), 201


def get_file(id):
    return File.get(id)


def delete_file(id):
    return File.delete(id), 204


def download_file(id):
    file = File.get(id)
    response = send_file(
        os.path.join(current_app.config["FILES_BASE_DIR"], str(file["id"])),
        attachment_filename=file["name"],
    )
    response.direct_passthrough = False
    return response
