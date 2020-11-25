from nucleus.controllers.base import BaseController
from nucleus.controllers.profiles import profile_controller
from nucleus.models.users import Roles as RolesModel
from nucleus.models.users import Users as UsersModel


class User(BaseController):
    """Management of the user."""

    def create(self, new_user: dict) -> UsersModel:
        if not new_user.get("role"):
            role = RolesModel.query.filter_by(name="user").first()
            new_user = {**new_user, "role_id": role.id}
        else:
            role = RolesModel.query.filter_by(name=new_user["role"]).first()
            del new_user["role"]
            new_user = {**new_user, "role_id": role.id}

        new_user_from_db = self.model_manager.create(new_user)

        profile_controller.create(
            {"name": "user", "lastname": "user", "user_id": new_user_from_db.id}
        )

        return self.model_manager.get(new_user_from_db.id)


user_controller = User(UsersModel)
role_controller = BaseController(RolesModel)
