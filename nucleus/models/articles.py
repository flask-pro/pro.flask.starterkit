from nucleus.common.extensions import db
from nucleus.models.base import Base


class Articles(Base):
    __filterable__ = ["author"]
    __files__ = ["main_picture_id", "main_video_id", "author_picture_id"]

    title = db.Column(db.String, comment="Title")
    announce = db.Column(db.Text, comment="Announce")
    content = db.Column(db.Text, comment="Content")
    main_picture_id = db.Column(db.String, db.ForeignKey("files.id"), comment="Main picture")
    main_video_id = db.Column(db.String, db.ForeignKey("files.id"), comment="Main video")
    author = db.Column(db.String, comment="Author")
    author_picture_id = db.Column(db.String, db.ForeignKey("files.id"), comment="Author picture")
    global_name = db.Column(db.String, unique=True, comment="Global name")

    main_picture = db.relationship(
        "Files", backref="main_picture_articles", foreign_keys=[main_picture_id], uselist=False
    )
    main_video = db.relationship(
        "Files", backref="main_video_articles", foreign_keys=[main_video_id], uselist=False
    )
    author_picture = db.relationship(
        "Files", backref="author_picture_articles", foreign_keys=[author_picture_id], uselist=False
    )

    def to_dict(self) -> dict:
        article = {
            "id": self.id,
            "title": self.title,
            "announce": self.announce,
            "content": self.content,
            "author": self.author,
            "datetime_created": self.datetime_created,
            "global_name": self.global_name,
            "main_picture": self.main_picture.to_dict() if self.main_picture else None,
            "main_video": self.main_video.to_dict() if self.main_video else None,
            "author_picture": self.author_picture.to_dict() if self.author_picture else None,
        }
        return self.non_empty_parameters_to_dict(article)

    def announce_to_dict(self) -> dict:
        article = {
            "id": self.id,
            "title": self.title,
            "announce": self.announce,
            "author": self.author,
            "datetime_created": self.datetime_created,
            "main_picture": self.main_picture.to_dict() if self.main_picture else None,
            "author_picture": self.author_picture.to_dict() if self.author_picture else None,
        }
        return self.non_empty_parameters_to_dict(article)

    def dict_to_search(self) -> dict:
        article = {
            "title": self.title,
            "announce": self.announce,
            "content": self.content,
            "author": self.author,
        }
        return self.non_empty_parameters_to_dict(article)
