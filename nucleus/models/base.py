from datetime import datetime

from nucleus.models import db


class Base(db.Model):
    """Base class for table.

    * **id** - Integer - unique identifier

    * **description** - Text - Description of the object

    * **datetime_created** - DateTime - Date and time of row create

    * **datetime_modified** - DateTime - Date and time of row update
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, index=True, comment="ID")
    description = db.Column(db.Text, comment="Description")
    datetime_created = db.Column(db.DateTime, default=datetime.utcnow(), comment="Date create")
    datetime_modified = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), comment="Date modified"
    )
