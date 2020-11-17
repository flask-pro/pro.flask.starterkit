from werkzeug.security import generate_password_hash

from nucleus.common.extensions import db
from nucleus.models.base import Base


class Users(Base):
    username = db.Column(db.String, nullable=False, unique=True, comment="Username")
    password_hash = db.Column(db.String, nullable=False, comment="Password")
    role_id = db.Column(db.String, db.ForeignKey("roles.id"), nullable=False)

    profiles = db.relationship("Profiles", backref="users", uselist=False)

    @property
    def password(self) -> None:
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def to_dict(self) -> dict:
        user = {
            "id": self.id,
            "username": self.username,
            "role": self.roles.name,
            "profile_id": self.profiles.id,
        }
        return self.non_empty_parameters_to_dict(user)


class Roles(Base):
    name = db.Column(db.String, nullable=False, unique=True, comment="Username")
    users = db.relationship("Users", backref="roles")

    @classmethod
    def bulk_create(cls, roles: list) -> list:
        role_objects = []
        for role in roles:
            new_role = Roles(**role)
            role_objects.append(new_role)
        db.session.add_all(role_objects)
        db.session.commit()
        return [role.to_dict() for role in role_objects]

    def to_dict(self) -> dict:
        role = {"id": self.id, "name": self.name, "description": self.description}
        return self.non_empty_parameters_to_dict(role)
