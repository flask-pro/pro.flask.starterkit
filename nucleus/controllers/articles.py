from nucleus.common.search import FulltextSearch
from nucleus.controllers.base import BaseController
from nucleus.controllers.files import file_controller
from nucleus.models.articles import Articles as ArticlesModel


class Article(BaseController):
    """Глобальное управление статьями."""

    def get_global_articles(self) -> list:
        global_articles = ArticlesModel.query.filter(ArticlesModel.global_name.isnot(None)).all()
        return global_articles

    def delete(self, id_: str) -> None:
        article = self.model_manager.delete(id_)

        if article.main_picture_id:
            file_controller.delete(article.main_picture_id)
        if article.main_video_id:
            file_controller.delete(article.main_video_id)
        if article.author_picture_id:
            file_controller.delete(article.author_picture_id)

        FulltextSearch.remove_from_index(article)


article_controller = Article(ArticlesModel)
