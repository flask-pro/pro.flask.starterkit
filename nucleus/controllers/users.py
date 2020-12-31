from nucleus.controllers.base import BaseController
from nucleus.controllers.logs import log_controller
from nucleus.controllers.profiles import profile_controller
from nucleus.models.users import Roles as RolesModel
from nucleus.models.users import Users as UsersModel

DEFAULT_USER_ROLE = "user"


class User(BaseController):
    """Management of the user."""

    def create(self, new_user: dict) -> UsersModel:
        if not new_user.get("role"):
            role = RolesModel.query.filter_by(name=DEFAULT_USER_ROLE).first()
            new_user = {**new_user, "role_id": role.id}
        else:
            role = RolesModel.query.filter_by(name=new_user["role"]).first()
            del new_user["role"]
            new_user = {**new_user, "role_id": role.id}

        new_user_from_db = self.model_manager.create(new_user)

        profile_controller.create(
            {"name": "user", "lastname": "user", "user_id": new_user_from_db.id}
        )

        log_controller.create({"email": new_user_from_db.email, "event": "user_created"})

        return self.model_manager.get(new_user_from_db.id)

    def delete(self, id_: str) -> UsersModel:
        deleted_user = self.model_manager.delete(id_)
        log_controller.create({"email": deleted_user.email, "event": "user_deleted"})
        return deleted_user

    def block(self, id_: str) -> UsersModel:
        blocked_user = self.model_manager.patch({"id": id_, "is_blocked": True})
        log_controller.create({"email": blocked_user.email, "event": "user_blocked"})
        return blocked_user

    def unblock(self, id_: str) -> UsersModel:
        unblocked_user = self.model_manager.patch({"id": id_, "is_blocked": False})
        log_controller.create({"email": unblocked_user.email, "event": "user_unblocked"})
        return unblocked_user


user_controller = User(UsersModel)
role_controller = BaseController(RolesModel)
