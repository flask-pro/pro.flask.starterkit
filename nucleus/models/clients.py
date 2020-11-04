from nucleus.models import db
from nucleus.models.base import Base


class Clients(Base):
    __searchable__ = ["name", "last_name", "mobile_phone", "description"]

    name = db.Column(db.String, nullable=False, comment="Name")
    last_name = db.Column(db.String, nullable=False, comment="Last name")
    mobile_phone = db.Column(db.String, nullable=False, unique=True, comment="Mobile phone")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "mobile_phone": self.mobile_phone,
            "description": self.description,
        }
