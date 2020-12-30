from nucleus.controllers.base import BaseController
from nucleus.models.articles import Articles as ArticlesModel
from nucleus.models.directories import Categories as CategoriesModel


class Directory:
    @classmethod
    def _get_global_articles(cls) -> dict:
        global_articles = ArticlesModel.query.filter(ArticlesModel.global_name.isnot(None)).all()
        return {article.global_name: article.to_dict() for article in global_articles}

    @classmethod
    def _get_categories(cls, content_type: str) -> list:
        categories = CategoriesModel.query.filter_by(content_type=content_type).all()
        return [item.to_dict() for item in categories]

    @classmethod
    def get_directories(cls):
        return {
            "feedbacks": {"categories": cls._get_categories("feedbacks")},
            "articles": cls._get_global_articles(),
        }


categories_controller = BaseController(CategoriesModel)
