from nucleus.common.extensions import db
from nucleus.models.base import Base


class Files(Base):
    name = db.Column(db.String, nullable=False, comment="File name")
    length = db.Column(db.Integer, nullable=True, comment="File length.")
    mime_type = db.Column(db.String, nullable=False, comment="File MIME type.")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "length": self.length,
            "mime_type": self.mime_type,
            "url": f"/v1/files/download/{self.id}",
            "thumbnail": f"/v1/files/download/{self.id}/thumbnail/",
        }
