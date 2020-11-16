from flask import abort
from flask import current_app

from nucleus.controllers.utils import Items
from nucleus.controllers.utils import ModelManager
from nucleus.models.profiles import Profiles as ProfilesModel


class Profile:
    """Management of the profile."""

    TABLE_MODEL = ModelManager(ProfilesModel)

    @staticmethod
    def get_profiles_list(parameters: dict) -> dict:
        ITEMS_PER_PAGE = current_app.config["ITEMS_PER_PAGE"]
        MAX_PER_PAGE = current_app.config["MAX_PER_PAGE"]

        profiles_list = Items(
            model=ProfilesModel, include_metadata=parameters.get("include_metadata", False)
        )
        profiles_list.ITEMS_PER_PAGE = ITEMS_PER_PAGE
        profiles_list.MAX_PER_PAGE = MAX_PER_PAGE
        profiles_list = profiles_list.result(
            int(parameters.get("page", 1)), int(parameters.get("per_page", ITEMS_PER_PAGE))
        )

        return profiles_list

    @classmethod
    def create(cls, profile: dict) -> ProfilesModel:
        return cls.TABLE_MODEL.create(profile)

    @classmethod
    def get(cls, id_: str) -> ProfilesModel:
        return cls.TABLE_MODEL.get(id_)

    @classmethod
    def update(cls, id_: str, profile: dict) -> ProfilesModel:
        if id_ != profile.get("id"):
            abort(400, "ID is required!")
        return cls.TABLE_MODEL.update(id_, profile)

    @classmethod
    def delete(cls, id_: str) -> dict:
        if cls.TABLE_MODEL.delete(id_):
            return ""
        else:
            abort(404, "Object not found!")
