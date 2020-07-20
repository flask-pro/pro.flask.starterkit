import connexion
from flask import request

from nucleus.controllers.users import User


def get_users_list():
    return User.users_list(connexion.request.args)


def create_user():
    return User.create(request.json), 201


def get_user(id):
    return User.get(id)


def update_user(id):
    return User.update(id, request.json)


def delete_user(id):
    User.delete(id)
    return '', 204
