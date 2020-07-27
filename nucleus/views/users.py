import connexion
from flask import request

from nucleus.controllers.users import User, Role


def get_users_list():
    return User.users_list(connexion.request.args)


def create_user():
    return User.create(request.json), 201


def get_user(id):
    return User.get(id)


def update_user(id):
    return User.update(id, request.json)


def delete_user(id):
    return User.delete(id), 204


def get_roles_list():
    return Role.roles_list(connexion.request.args)


def create_role():
    return Role.create(request.json), 201


def get_role(id):
    return Role.get(id)


def update_role(id):
    return Role.update(id, request.json)


def delete_role(id):
    return Role.delete(id), 204
