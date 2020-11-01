import os

import connexion
from flask import current_app
from flask import send_file

from nucleus.common.decorators import role_admin_or_user_required
from nucleus.common.decorators import role_admin_required
from nucleus.controllers.files import File


@role_admin_required
def file_list():
    return File.file_list(connexion.request.args)


@role_admin_required
def upload_file():
    return File.create(connexion.request.files.get("file")), 201


@role_admin_required
def get_file(id):
    return File.get(id)


@role_admin_required
def delete_file(id):
    return File.delete(id), 204


@role_admin_or_user_required
def download_file(id):
    file = File.get(id)
    response = send_file(
        os.path.join(current_app.config["FILES_BASE_DIR"], str(file["id"])),
        attachment_filename=file["name"],
    )
    response.direct_passthrough = False
    return response
