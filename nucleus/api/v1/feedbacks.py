from typing import Tuple

import connexion

from nucleus.api.v1.utils import args_to_dict
from nucleus.api.v1.utils import check_to_equality
from nucleus.common.decorators import role_admin_required
from nucleus.controllers.feedbacks import feedback_controller


@role_admin_required
def get_feedbacks_list() -> dict:
    args = args_to_dict(connexion.request.args)
    return feedback_controller.get_list(args)


@role_admin_required
def create_feedback() -> Tuple:
    return feedback_controller.create(connexion.request.json).to_dict(), 201


def get_feedback(id) -> dict:
    return feedback_controller.get(id).to_dict()


@role_admin_required
def update_feedback(id) -> dict:
    parameters = connexion.request.json
    check_to_equality(id, "id", parameters)
    return feedback_controller.update(parameters).to_dict()


@role_admin_required
def delete_feedback(id) -> Tuple:
    feedback_controller.delete(id)
    return None, 204
