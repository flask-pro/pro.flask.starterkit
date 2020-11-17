import time

from flask import abort
from flask import current_app
from jose import jwt
from werkzeug.security import check_password_hash

from nucleus.controllers.users import User
from nucleus.models.users import Users


class Auth:
    @staticmethod
    def _current_timestamp() -> int:
        return int(time.time())

    @staticmethod
    def generate_auth_token(id_: str, expiries_in: int) -> str:
        timestamp = Auth._current_timestamp()
        payload = {
            "iss": current_app.config["JWT_ISSUER"],
            "iat": int(timestamp),
            "exp": int(timestamp + expiries_in),
            "sub": id_,
        }

        return jwt.encode(
            payload, current_app.config["JWT_SECRET"], algorithm=current_app.config["JWT_ALGORITHM"]
        )

    @classmethod
    def get_token(cls, id_: str) -> dict:
        access_token = cls.generate_auth_token(id_, current_app.config["JWT_ACCESS_TOKEN_LIFETIME"])
        refresh_token = cls.generate_auth_token(
            id_, current_app.config["JWT_REFRESH_TOKEN_LIFETIME"]
        )

        token_dict = {"access_token": access_token, "refresh_token": refresh_token}

        return token_dict

    @classmethod
    def login(cls, username: str, password: str) -> [int, dict]:
        user = Users.query.filter_by(username=username).first()
        if user is None:
            abort(400, f"User NOT exist! | username: <{username}>")
        elif check_password_hash(user.password_hash, password):
            return cls.get_token(user.id)
        else:
            abort(400, f"Password wrong! | username: <{username}>")

    @classmethod
    def signup(cls, user: dict) -> dict:
        return User.create(user).to_dict()
