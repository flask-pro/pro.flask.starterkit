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
                value = parameters[field]
                if type(value) is list:
                    self._query = self._query.filter(getattr(self._model, field).in_(value))
                else:
                    self._query = self._query.filter_by(**{field: value})

    def _interval_filtration(self, parameters: dict) -> None:
        for field in self._model.__interval_filterable__:
            start_field = f"start_{field}"
            if start_field in parameters:
                value = parameters[start_field]
                self._query = self._query.filter(getattr(self._model, field) >= value)

            end_field = f"end_{field}"
            if end_field in parameters:
                value = parameters[end_field]
                self._query = self._query.filter(getattr(self._model, field) < value)

    def _sorting(self, parameters: dict) -> None:
        """Добавление условий сортировки в запрос."""

        sorting_parameters = {
            key.replace("sort_", ""): value
            for key, value in parameters.items()
            if key.startswith("sort_") and key.replace("sort_", "") in self._model.__sortable__
        }

        if not sorting_parameters:
            self._query = self._query.order_by(getattr(self._model, "datetime_created"))
        else:
            for key, value in sorting_parameters.items():
                if value == "asc":
                    self._query = self._query.order_by(getattr(self._model, key))
                elif value == "desc":
                    self._query = self._query.order_by(getattr(self._model, key).desc())

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
        self._interval_filtration(parameters)
        self._sorting(parameters)

        result = self._pagination(parameters).items

        if announce:
            items = {"items": [item.announce_to_dict() for item in result]}
        else:
            items = {"items": [item.to_dict() for item in result]}

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

    def update(self, parameters: dict) -> db.Model:
        return self.patch(parameters)

    def patch(self, parameters: dict) -> db.Model:
        row = self._model.query.filter_by(id=parameters["id"]).one()
        if parameters.get("id"):
            del parameters["id"]
        for key, value in parameters.items():
            setattr(row, key, value)
        db.session.commit()
        return row

    def delete(self, id_: str) -> db.Model:
        row = self._model.query.filter_by(id=id_).one()
        db.session.delete(row)
        db.session.commit()
        return row
