from nucleus.common.errors import NoResultSearch
from nucleus.common.external.elastic import FulltextSearch
from nucleus.config import Config
from nucleus.models.articles import Articles as ArticlesModel

ITEMS_PER_PAGE = Config.ITEMS_PER_PAGE


class Search:
    """Management of the search."""

    MODELS_MAP = {"articles": ArticlesModel}

    @classmethod
    def results_list(cls, parameters: dict) -> dict:

        model = cls.MODELS_MAP.get(parameters["scope"])

        if parameters["scope"] in ["elements", "games", "exercises"]:
            fields_to_filter = {"type": parameters["scope"]}
        else:
            fields_to_filter = None

        if model:
            ids, pagination = FulltextSearch.query_index(
                model,
                parameters["q"],
                int(parameters.get("page", 1)),
                int(parameters.get("per_page", ITEMS_PER_PAGE)),
                fields_to_filter=fields_to_filter,
            )
        else:
            raise NoResultSearch(f"Model <{model}> not allow to search. | parameters: {parameters}")

        items = [item.to_dict() for item in model.query.filter(model.id.in_(ids)).all()]
        result = {"items": items}

        if parameters.get("include_metadata", False):
            result["_metadata"] = {
                "pagination": {
                    "page": parameters.get("page", 1),
                    "per_page": parameters.get("per_page", ITEMS_PER_PAGE),
                    "pages": 0,
                    "items": pagination["value"],
                }
            }
        return result

    @classmethod
    def reindex(cls, parameters: dict) -> str:
        model = cls.MODELS_MAP.get(parameters["scope"])

        items = model.query.all()
        for item in items:
            FulltextSearch.add_to_index(item)

        return "OK"
