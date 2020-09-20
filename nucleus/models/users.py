import sqlalchemy
from flask import abort
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

    @classmethod
    def create(cls, user: dict) -> dict:
        create_user = Users(**user)
        db.session.add(create_user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            abort(422, f'User exist: <{user["username"]}>')
        return create_user.to_dict()

    @classmethod
    def get(cls, id_: int) -> dict:
        user = Users.query.filter_by(id=id_).one()
        return user.to_dict()

    @classmethod
    def update(cls, user: dict) -> dict:
        new_user = Users.query.filter_by(id=user["id"]).one()
        new_user.username = user["username"]
        db.session.commit()
        return new_user.to_dict()

    @classmethod
    def delete(cls, id_: int) -> None:
        return Users.query.filter_by(id=id_).delete()

    def to_dict(self) -> dict:
        return {"id": self.id, "username": self.username}


class Roles(Base):
    name = db.Column(db.String, nullable=False, comment="Username")
    users = db.relationship("Users", backref="roles")

    @classmethod
    def create(cls, role: dict) -> dict:
        create_role = Roles(**role)
        db.session.add(create_role)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            abort(422, f'Role exist: <{role["name"]}>')
        return create_role.to_dict()

    @classmethod
    def get(cls, id_: int) -> dict:
        role = Roles.query.filter_by(id=id_).one()
        return role.to_dict()

    @classmethod
    def update(cls, role: dict) -> dict:
        new_role = Roles.query.filter_by(id=role["id"]).one()
        new_role.name = role["name"]
        new_role.description = role["description"]
        db.session.commit()
        return new_role.to_dict()

    @classmethod
    def delete(cls, id_: int) -> None:
        return Roles.query.filter_by(id=id_).delete()

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
