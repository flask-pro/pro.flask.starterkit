from flask_sqlalchemy import Pagination

from nucleus.common.extensions import db
from nucleus.config import Config

ITEMS_PER_PAGE = Config.ITEMS_PER_PAGE
MAX_PER_PAGE = Config.MAX_PER_PAGE


class Items:
    def __init__(self, model: db.Model, include_metadata: bool = False) -> None:
        self._model = model
        self._query = model.query
        self._metadata = {}
        self.include_metadata = include_metadata

    def _filtration(self, parameters: dict) -> None:
        """Добавление условий фильтрации в запрос."""

        for field in self._model.__filterable__:
            if field in parameters:
                self._query = self._query.filter_by(**{field: parameters[field]})

    def _pagination(self, parameters: dict) -> Pagination:
        """Create pagination object."""

        page = int(parameters.get("page", 1))
        per_page = int(parameters.get("per_page", ITEMS_PER_PAGE))

        paginated_query = self._query.paginate(
            page=page, per_page=per_page, max_per_page=MAX_PER_PAGE
        )
        if self.include_metadata:
            self._metadata["pagination"] = {
                "page": paginated_query.page,
                "per_page": paginated_query.per_page,
                "pages": paginated_query.pages,
                "items": paginated_query.total,
            }
        return paginated_query

    def result(self, parameters: dict, announce: bool = False) -> dict:
        """Make query result."""

        self._filtration(parameters)
        paginated_result = self._pagination(parameters)

        if announce:
            items = {"items": [item.announce_to_dict() for item in paginated_result.items]}
        else:
            items = {"items": [item.to_dict() for item in paginated_result.items]}
        if self.include_metadata:
            items["_metadata"] = self._metadata

        return items


class ModelManager:
    def __init__(self, model: db.Model):
        self._model = model

    def create(self, params: dict) -> db.Model:
        new_row = self._model(**params)
        db.session.add(new_row)
        db.session.commit()
        return new_row

    def get(self, id_: str) -> db.Model:
        return self._model.query.filter_by(id=id_).one()

    def get_all_items(self) -> db.Model:
        return self._model.query.all()

    def update(self, id_: str, params: dict) -> db.Model:
        return self.patch(id_, params)

    def patch(self, id_: str, params: dict) -> db.Model:
        row = self._model.query.filter_by(id=id_).one()
        if params.get("id"):
            del params["id"]
        for key, value in params.items():
            setattr(row, key, value)
        db.session.commit()
        return row

    def delete(self, id_: str) -> None:
        row = self._model.query.filter_by(id=id_).one()
        db.session.delete(row)
        db.session.commit()
        return row
