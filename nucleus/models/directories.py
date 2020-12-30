from nucleus.common.extensions import db
from nucleus.models.base import Base


class Categories(Base):
    __table_args__ = (db.UniqueConstraint("name", "content_type"),)
    __filterable__ = ["content_type"]
    __files__ = ["icon_id"]

    name = db.Column(db.String, comment="Name")
    content_type = db.Column(db.String, nullable=False, comment="Content type")
    icon_id = db.Column(db.String, db.ForeignKey("files.id"), comment="Icon picture")

    icon = db.relationship("Files", backref="icon_category", uselist=False)

    def to_dict(self) -> dict:
        category = {
            "id": self.id,
            "icon": self.icon.to_dict() if self.icon else None,
            "name": self.name,
            "content_type": self.content_type,
        }
        return self.non_empty_parameters_to_dict(category)
