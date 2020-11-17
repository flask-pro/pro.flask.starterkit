import uuid
from datetime import datetime

from nucleus.common.extensions import db
from nucleus.common.search import FullTextSearchMixin


def make_uuid4() -> str:
    return str(uuid.uuid4())


class Base(FullTextSearchMixin, db.Model):
    """Base class for table.

    * **id** - Integer - unique identifier

    * **description** - Text - Description of the object

    * **datetime_created** - DateTime - Date and time of row create

    * **datetime_modified** - DateTime - Date and time of row update
    """

    __abstract__ = True

    __searchable__ = ["description"]
    __filterable__ = ["id"]
    __sortable__ = ["datetime_created"]

    id = db.Column(db.String, primary_key=True, index=True, default=make_uuid4, comment="ID")
    description = db.Column(db.Text, comment="Description")
    datetime_created = db.Column(db.DateTime, default=datetime.utcnow(), comment="Date create")
    datetime_modified = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), comment="Date modified"
    )

    @classmethod
    def non_empty_parameters_to_dict(cls, parameters: dict) -> dict:
        return {key: value for key, value in parameters.items() if value}

    def __repr__(self):
        parameters = ", ".join([f"{key}={value}" for key, value in self.to_dict().items()])
        return f"{self.__class__.__name__}({parameters})"
