from flask import abort, current_app

from nucleus.controllers.utils import Items
from nucleus.models.users import Users, Roles


class User:
    """Management of the user."""

    @staticmethod
    def users_list(parameters: dict) -> dict:
        ITEMS_PER_PAGE = current_app.config['ITEMS_PER_PAGE']
        MAX_PER_PAGE = current_app.config['MAX_PER_PAGE']

        users_list = Items(model=Users,
                           include_metadata=parameters.get('include_metadata', False))
        users_list.ITEMS_PER_PAGE = ITEMS_PER_PAGE
        users_list.MAX_PER_PAGE = MAX_PER_PAGE
        users_list = users_list.result(int(parameters.get('page', 1)),
                                       int(parameters.get('per_page', ITEMS_PER_PAGE)))

        return users_list

    @classmethod
    def create(cls, user: dict) -> dict:
        if not user.get('role'):
            role = Roles.query.filter_by(name='user').first()
            user = {**user, 'role_id': role.id}
        else:
            role = Roles.query.filter_by(name=user['role']).first()
            del user['role']
            user = {**user, 'role_id': role.id}

        return Users.create(user)

    @classmethod
    def get(cls, id_: int) -> dict:
        return Users.get(id_)

    @classmethod
    def update(cls, id_: int, user: dict) -> dict:
        if id_ != user.get('id'):
            abort(400, 'ID is required!')
        return Users.update(user)

    @classmethod
    def delete(cls, id_: int) -> dict:
        if Users.delete(id_):
            return ''
        else:
            abort(404, 'Object not found!')


class Role:
    """Management of the role."""

    @staticmethod
    def roles_list(parameters: dict) -> dict:
        ITEMS_PER_PAGE = current_app.config['ITEMS_PER_PAGE']
        MAX_PER_PAGE = current_app.config['MAX_PER_PAGE']

        roles_list = Items(model=Roles,
                           include_metadata=parameters.get('include_metadata', False))
        roles_list.ITEMS_PER_PAGE = ITEMS_PER_PAGE
        roles_list.MAX_PER_PAGE = MAX_PER_PAGE
        roles_list = roles_list.result(int(parameters.get('page', 1)),
                                       int(parameters.get('per_page', ITEMS_PER_PAGE)))

        return roles_list

    @classmethod
    def create(cls, role: dict) -> dict:
        return Roles.create(role)

    @classmethod
    def get(cls, id_: int) -> dict:
        return Roles.get(id_)

    @classmethod
    def update(cls, id_: int, role: dict) -> dict:
        if id_ != role.get('id'):
            abort(400, 'ID is required!')
        return Roles.update(role)

    @classmethod
    def delete(cls, id_: int) -> dict:
        if Roles.delete(id_):
            return ''
        else:
            abort(404, 'Object not found!')
