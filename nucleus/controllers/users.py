from flask import abort

from nucleus.models.users import Users


class User:
    """Management of the user."""

    @classmethod
    def create(cls, user: dict):
        if not user.get('username'):
            abort(400, 'Username is required!')
        new_user = Users.create(user)
        return new_user

    @classmethod
    def get(cls, id_: int):
        return Users.get(id_)

    @classmethod
    def update(cls, id_: int, user: dict):
        if id_ != user.get('id'):
            abort(400, 'ID is required!')
        if not user.get('username'):
            abort(400, 'Username is required!')

        new_user = Users.update(user)

        return new_user

    @classmethod
    def delete(cls, id_: int):
        return Users.delete(id_)
