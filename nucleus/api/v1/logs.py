import connexion

from nucleus.api.v1.utils import args_to_datetime
from nucleus.api.v1.utils import args_to_dict
from nucleus.common.decorators import role_admin_required
from nucleus.controllers.logs import log_controller


@role_admin_required
def get_logs_list() -> dict:
    args = args_to_dict(connexion.request.args)
    args = args_to_datetime(args, ["start_datetime_created", "end_datetime_created"])
    return log_controller.get_list(args)
