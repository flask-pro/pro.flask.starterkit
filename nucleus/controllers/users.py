from flask import abort
from flask import current_app

from nucleus.controllers.profiles import Profile
from nucleus.controllers.utils import Items
from nucleus.controllers.utils import ModelManager
from nucleus.models.users import Roles as RolesModel
from nucleus.models.users import Users as UsersModel


class User:
    """Management of the user."""

    TABLE_MODEL = ModelManager(UsersModel)

    @staticmethod
    def get_users_list(parameters: dict) -> dict:
        ITEMS_PER_PAGE = current_app.config["ITEMS_PER_PAGE"]
        MAX_PER_PAGE = current_app.config["MAX_PER_PAGE"]

        users_list = Items(
            model=UsersModel, include_metadata=parameters.get("include_metadata", False)
        )
        users_list.ITEMS_PER_PAGE = ITEMS_PER_PAGE
        users_list.MAX_PER_PAGE = MAX_PER_PAGE
        users_list = users_list.result(
            int(parameters.get("page", 1)), int(parameters.get("per_page", ITEMS_PER_PAGE))
        )

        return users_list

    @classmethod
    def create(cls, new_user: dict) -> UsersModel:
        if not new_user.get("role"):
            role = RolesModel.query.filter_by(name="user").first()
            new_user = {**new_user, "role_id": role.id}
        else:
            role = RolesModel.query.filter_by(name=new_user["role"]).first()
            del new_user["role"]
            new_user = {**new_user, "role_id": role.id}

        new_user_from_db = cls.TABLE_MODEL.create(new_user)

        Profile.create({"name": "user", "lastname": "user", "user_id": new_user_from_db.id})

        return cls.TABLE_MODEL.get(new_user_from_db.id)

    @classmethod
    def get(cls, id_: str) -> UsersModel:
        return cls.TABLE_MODEL.get(id_)

    @classmethod
    def update(cls, id_: str, user: dict) -> UsersModel:
        if id_ != user.get("id"):
            abort(400, "ID is required!")
        return cls.TABLE_MODEL.update(id_, user)

    @classmethod
    def delete(cls, id_: str) -> dict:
        if cls.TABLE_MODEL.delete(id_):
            return ""
        else:
            abort(404, "Object not found!")


class Role:
    """Management of the role."""

    TABLE_MODEL = ModelManager(RolesModel)

    @staticmethod
    def roles_list(parameters: dict) -> dict:
        ITEMS_PER_PAGE = current_app.config["ITEMS_PER_PAGE"]
        MAX_PER_PAGE = current_app.config["MAX_PER_PAGE"]

        roles_list = Items(
            model=RolesModel, include_metadata=parameters.get("include_metadata", False)
        )
        roles_list.ITEMS_PER_PAGE = ITEMS_PER_PAGE
        roles_list.MAX_PER_PAGE = MAX_PER_PAGE
        roles_list = roles_list.result(
            int(parameters.get("page", 1)), int(parameters.get("per_page", ITEMS_PER_PAGE))
        )

        return roles_list

    @classmethod
    def create(cls, role: dict) -> RolesModel:
        return cls.TABLE_MODEL.create(role)

    @classmethod
    def get(cls, id_: str) -> RolesModel:
        return cls.TABLE_MODEL.get(id_)

    @classmethod
    def update(cls, id_: str, role: dict) -> RolesModel:
        if id_ != role.get("id"):
            abort(400, "ID is required!")
        return cls.TABLE_MODEL.update(id_, role)

    @classmethod
    def delete(cls, id_: str) -> dict:
        if cls.TABLE_MODEL.delete(id_):
            return ""
        else:
            abort(404, "Object not found!")
