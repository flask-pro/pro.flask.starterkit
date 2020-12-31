from werkzeug.security import generate_password_hash

from nucleus.common.extensions import db
from nucleus.models.base import Base


class Users(Base):
    email = db.Column(db.String, nullable=False, unique=True, comment="E-mail")
    mobile_phone = db.Column(db.String, unique=True, comment="Mobile phone")
    password_hash = db.Column(db.String, nullable=False, comment="Password")
    role_id = db.Column(db.String, db.ForeignKey("roles.id"), nullable=False)
    is_blocked = db.Column(db.Boolean, default=False, nullable=False, comment="Blocking sign")

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
            "email": self.email,
            "mobile_phone": self.mobile_phone,
            "role": self.roles.name,
            "profile_id": self.profiles.id,
            "is_blocked": self.is_blocked,
        }
        return self.non_empty_parameters_to_dict(user)


class Roles(Base):
    name = db.Column(db.String, nullable=False, unique=True, comment="Role name")
    users = db.relationship("Users", backref="roles")

    def to_dict(self) -> dict:
        role = {"id": self.id, "name": self.name, "description": self.description}
        return self.non_empty_parameters_to_dict(role)
