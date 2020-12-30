import os

import connexion
from flask import current_app
from flask import send_file

from nucleus.common.decorators import role_admin_or_user_required
from nucleus.common.decorators import role_admin_required
from nucleus.controllers.files import file_controller


@role_admin_required
def get_files_list():
    return file_controller.get_list(connexion.request.args)


@role_admin_required
def upload_file():
    return file_controller.create(connexion.request.files.get("file")).to_dict(), 201


@role_admin_required
def get_file(id):
    return file_controller.get(id).to_dict()


@role_admin_required
def delete_file(id):
    file_controller.delete(id)
    return None, 204


@role_admin_or_user_required
def download_file(id):
    file = file_controller.get(id)
    response = send_file(
        os.path.join(current_app.config["FILES_BASE_DIR"], file.id), attachment_filename=file.name
    )
    response.direct_passthrough = False
    return response


@role_admin_or_user_required
def download_thumbnail(id):
    file = file_controller.get(id)
    file_path = os.path.join(current_app.config["FILES_BASE_DIR"], "thumbnails", file.id)

    try:
        response = send_file(file_path, attachment_filename=file.name)
    except FileNotFoundError:
        response = send_file(
            current_app.config["DEFAULT_THUMBNAIL"], attachment_filename="thumbnail.jpg"
        )

    response.direct_passthrough = False
    return response


def cdn_download_file(id):
    file = file_controller.get(id)
    response = send_file(
        os.path.join(current_app.config["FILES_BASE_DIR"], file.id), attachment_filename=file.name
    )
    response.direct_passthrough = False
    return response


def cdn_download_thumbnail(id):
    file = file_controller.get(id)
    file_path = os.path.join(current_app.config["FILES_BASE_DIR"], "thumbnails", file.id)

    try:
        response = send_file(file_path, attachment_filename=file.name)
    except FileNotFoundError:
        response = send_file(
            current_app.config["DEFAULT_THUMBNAIL"], attachment_filename="thumbnail.jpg"
        )

    response.direct_passthrough = False
    return response
