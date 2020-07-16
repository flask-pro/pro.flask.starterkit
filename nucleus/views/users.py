from flask import request

from nucleus.controllers.users import User


def registration_user_routes(app):
    @app.route('/users', methods=['POST'])
    def create_user():
        return User.create(request.json), 201

    @app.route('/users/<int:id>', methods=['GET'])
    def get_user(id):
        return User.get(id)

    @app.route('/users/<int:id>', methods=['PUT'])
    def update_user(id):
        return User.update(id, request.json)

    @app.route('/users/<int:id>', methods=['DELETE'])
    def delete_user(id):
        User.delete(id)
        return '', 204

    return app
