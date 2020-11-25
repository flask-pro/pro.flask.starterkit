from nucleus.common.extensions import db
from nucleus.models.base import Base


class Profiles(Base):
    __sortable__ = ["name", "lastname"]

    name = db.Column(db.String, comment="Name")
    lastname = db.Column(db.String, comment="Lastname")
    user_id = db.Column(db.String, db.ForeignKey("users.id"), unique=True, nullable=True)

    def to_dict(self) -> dict:
        profile = {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "user_id": self.user_id,
            "description": self.description,
        }
        return self.non_empty_parameters_to_dict(profile)
