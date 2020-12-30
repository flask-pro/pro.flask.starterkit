from nucleus.controllers.base import BaseController
from nucleus.models.articles import Articles as ArticlesModel

article_controller = BaseController(ArticlesModel)
