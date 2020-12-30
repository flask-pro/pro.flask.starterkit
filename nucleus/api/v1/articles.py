from typing import Tuple

import connexion

from nucleus.api.v1.utils import check_to_equality
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
    parameters = connexion.request.json
    check_to_equality(id, "id", parameters)
    return article_controller.update(parameters).to_dict()


@role_admin_required
def delete_article(id) -> Tuple:
    article_controller.delete(id)
    return None, 204
