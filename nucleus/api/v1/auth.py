from typing import Tuple

from flask import abort
from flask import current_app
from flask import request
from jose import jwt
from jose import JWTError

from nucleus.controllers.auth import Auth
from nucleus.controllers.users import User


def decode_token(token):
    try:
        return jwt.decode(
            token,
            current_app.config["JWT_SECRET"],
            algorithms=[current_app.config["JWT_ALGORITHM"]],
        )
    except JWTError:
        abort(401, "Token broken!")


def basic_auth(username, password, required_scopes=None) -> dict:
    return {"sub": Auth.login(username, password)}


def signup() -> Tuple[dict, int]:
    return User.create(request.json), 201


def login(user) -> Tuple[dict, int]:
    return user, 201


def profile(token_info) -> dict:
    return User.get(token_info["sub"])


def renew(token_info) -> Tuple[dict, int]:
    return Auth.get_token(token_info["sub"]), 201
