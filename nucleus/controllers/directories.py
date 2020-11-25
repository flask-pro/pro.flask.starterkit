from nucleus.controllers.articles import article_controller


class Directory:
    @classmethod
    def get_directories(cls):
        global_articles = {
            article.global_name: article.to_dict()
            for article in article_controller.get_global_articles()
        }
        return {"articles": global_articles}
