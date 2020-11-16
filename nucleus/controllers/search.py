from flask import current_app

from nucleus.common.errors import NoResultSearch
from nucleus.models.clients import Clients as ClientsModel


class Search:
    """Management of the search."""

    MODELS_MAP = {"clients": ClientsModel}

    @classmethod
    def results_list(cls, parameters: dict) -> dict:
        ITEMS_PER_PAGE = current_app.config["ITEMS_PER_PAGE"]

        model = cls.MODELS_MAP.get(parameters["scope"])

        if model:
            query = model.search(
                parameters["q"],
                int(parameters.get("page", 1)),
                int(parameters.get("per_page", ITEMS_PER_PAGE)),
            )
        else:
            raise NoResultSearch(f"Model <{model}> not allow to search. | parameters: {parameters}")

        items = [item.to_dict() for item in query[0].all()]
        result = {"items": items}

        if parameters.get("include_metadata", False):
            result["_metadata"] = {
                "pagination": {
                    "page": parameters.get("page", 1),
                    "per_page": parameters.get("per_page", ITEMS_PER_PAGE),
                    "pages": 0,
                    "items": query[1]["value"],
                }
            }
        return result

    @classmethod
    def reindex(cls, parameters: dict) -> str:
        model = cls.MODELS_MAP.get(parameters["scope"])

        if model:
            model.reindex()
        else:
            raise NoResultSearch(
                f"Model <{model}> not allow to reindex. | parameters: {parameters}"
            )

        return "OK"
