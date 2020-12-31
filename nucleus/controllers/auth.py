import time

from flask import abort
from flask import current_app
from jose import jwt
from werkzeug.security import check_password_hash

from nucleus.controllers.logs import log_controller
from nucleus.controllers.users import user_controller
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
    def login(cls, email: str, password: str) -> [int, dict]:
        user = Users.query.filter_by(email=email).first()
        if not user:
            abort(400, "Authorization failed!")
        elif user.is_blocked:
            abort(401, "User is blocked!")
        elif check_password_hash(user.password_hash, password):
            return cls.get_token(user.id)
        else:
            abort(400, "Authorization failed!")

    @classmethod
    def signup(cls, user: dict) -> dict:
        new_user = user_controller.create(user)
        log_controller.create({"email": new_user.email, "event": "user_signup"})
        return new_user.to_dict()
