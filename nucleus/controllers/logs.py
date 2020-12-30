from nucleus.controllers.base import BaseController
from nucleus.models.logs import Logs as LogsModel

log_controller = BaseController(LogsModel)
