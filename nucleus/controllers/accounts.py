from nucleus.controllers.profiles import Profile
from nucleus.controllers.users import User
from nucleus.models.profiles import Profiles as ProfilesModel


class Account:
    @classmethod
    def get_profile(cls, user_id: str) -> ProfilesModel:
        user = User.get(user_id)
        return Profile.get(user.profiles.id)
