from nucleus.common.extensions import db
from nucleus.models.base import Base


class Feedbacks(Base):
    __filterable__ = ["category_id"]

    email = db.Column(db.String, comment="E-mail")
    mobile_phone = db.Column(db.String, comment="Mobile phone")
    title = db.Column(db.String, comment="Title")
    message = db.Column(db.Text, comment="Message")
    category_id = db.Column(db.String, db.ForeignKey("categories.id"), comment="Category")

    category = db.relationship("Categories", backref="feedbacks", uselist=False)

    def to_dict(self) -> dict:
        article = {
            "id": self.id,
            "email": self.email,
            "mobile_phone": self.mobile_phone,
            "title": self.title,
            "message": self.message,
            "category_id": self.category_id,
        }
        return self.non_empty_parameters_to_dict(article)
