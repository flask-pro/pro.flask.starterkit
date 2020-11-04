from datetime import datetime

from nucleus.common.search import FullTextSearchMixin
from nucleus.models import db


class Base(FullTextSearchMixin, db.Model):
    """Base class for table.

    * **id** - Integer - unique identifier

    * **description** - Text - Description of the object

    * **datetime_created** - DateTime - Date and time of row create

    * **datetime_modified** - DateTime - Date and time of row update
    """

    __abstract__ = True

    __searchable__ = ["description"]

    id = db.Column(db.Integer, primary_key=True, index=True, comment="ID")
    description = db.Column(db.Text, comment="Description")
    datetime_created = db.Column(db.DateTime, default=datetime.utcnow(), comment="Date create")
    datetime_modified = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), comment="Date modified"
    )

    def to_dict(self) -> dict:
        return {key: getattr(self, key) for key in dir(self) if not key.startswith("_")}

    def __repr__(self):
        parameters = ", ".join([f"{key}={value}" for key, value in self.to_dict().items()])
        return f"{self.__class__.__name__}({parameters})"
