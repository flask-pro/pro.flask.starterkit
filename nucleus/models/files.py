from nucleus.common.extensions import db
from nucleus.config import Config
from nucleus.models.base import Base

CDN_BASE_URL = Config.CDN_BASE_URL


class Files(Base):
    name = db.Column(db.String, nullable=False, comment="File name")
    length = db.Column(db.Integer, nullable=True, comment="File length.")
    mime_type = db.Column(db.String, nullable=False, comment="File MIME type.")

    def to_dict(self) -> dict:
        file = {
            "id": self.id,
            "name": self.name,
            "length": self.length,
            "mime_type": self.mime_type,
            "url": f"/v1/files/download/{self.id}",
            "thumbnail": f"/v1/files/download/{self.id}/thumbnail",
        }
        if CDN_BASE_URL:
            file["url"] = f"{CDN_BASE_URL}/v1/files/cdn/{self.id}"
            file["thumbnail"] = f"{CDN_BASE_URL}/v1/files/cdn/{self.id}/thumbnail"
        return self.non_empty_parameters_to_dict(file)
