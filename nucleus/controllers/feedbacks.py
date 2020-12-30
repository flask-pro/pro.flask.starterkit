from nucleus.controllers.base import BaseController
from nucleus.models.feedbacks import Feedbacks as FeedbacksModel

feedback_controller = BaseController(FeedbacksModel)
