from nucleus.models import db


class Items:
    ITEMS_PER_PAGE = 30
    MAX_PER_PAGE = 100

    def __init__(self, model: db.Model, include_metadata: bool = False) -> None:
        self._query = model.query
        self._metadata = {}
        self.include_metadata = include_metadata

    def _pagination(self, page: int, per_page: int) -> None:
        """Create pagination object."""

        self._query = self._query.paginate(
            page=page, per_page=per_page, max_per_page=self.MAX_PER_PAGE
        )
        if self.include_metadata:
            self._metadata["pagination"] = {
                "page": self._query.page,
                "per_page": self._query.per_page,
                "pages": self._query.pages,
                "items": self._query.total,
            }

    def result(self, page: int = 1, per_page: int = None) -> dict:
        """Make query result."""

        if not per_page:
            per_page = self.ITEMS_PER_PAGE

        self._pagination(page, per_page)

        items = {"items": [item.to_dict() for item in self._query.items]}
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
        deleted_row_id = self._model.query.filter_by(id=id_).delete()
        db.session.commit()
        return deleted_row_id
