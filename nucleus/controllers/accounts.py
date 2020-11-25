from nucleus.controllers.profiles import profile_controller
from nucleus.controllers.users import user_controller
from nucleus.models.profiles import Profiles as ProfilesModel


class Account:
    @classmethod
    def get_profile(cls, user_id: str) -> ProfilesModel:
        user = user_controller.get(user_id)
        return profile_controller.get(user.profiles.id)
