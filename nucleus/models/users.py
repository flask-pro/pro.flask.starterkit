from werkzeug.security import generate_password_hash

from nucleus.models import db
from nucleus.models.base import Base


class Users(Base):
    username = db.Column(db.String, nullable=False, unique=True, comment="Username")
    password_hash = db.Column(db.String, nullable=False, comment="Password")
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

    @property
    def password(self) -> None:
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def to_dict(self) -> dict:
        return {"id": self.id, "username": self.username}


class Roles(Base):
    name = db.Column(db.String, nullable=False, comment="Username")
    users = db.relationship("Users", backref="roles")

    @classmethod
    def bulk_create(cls, roles: list) -> list:
        role_objects = []
        for role in roles:
            new_role = Roles(**role)
            role_objects.append(new_role)
        db.session.add_all(role_objects)
        db.session.commit()
        return [_.to_dict() for _ in role_objects]

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "description": self.description}
