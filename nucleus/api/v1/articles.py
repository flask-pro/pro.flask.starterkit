from typing import Tuple

import connexion

from nucleus.common.decorators import role_admin_required
from nucleus.controllers.articles import article_controller


def get_articles_list() -> dict:
    return article_controller.get_list(connexion.request.args, announce=True)


@role_admin_required
def create_article() -> Tuple:
    return article_controller.create(connexion.request.json).to_dict(), 201


def get_article(id) -> dict:
    return article_controller.get(id).to_dict()


@role_admin_required
def update_article(id) -> dict:
    return article_controller.update(id, connexion.request.json).to_dict()


@role_admin_required
def delete_article(id) -> Tuple:
    return article_controller.delete(id), 204
