from typing import Tuple

import connexion
from flask import abort
from flask import current_app
from flask import g
from jose import jwt
from jose import JWTError

from nucleus.common.decorators import role_admin_or_user_required
from nucleus.config import Config
from nucleus.controllers.auth import Auth
from nucleus.controllers.users import user_controller

CDN_SECRET = Config.CDN_SECRET


def decode_token(token) -> str:
    try:
        token = jwt.decode(
            token,
            current_app.config["JWT_SECRET"],
            algorithms=[current_app.config["JWT_ALGORITHM"]],
        )

        user = user_controller.get(token["sub"])

        if user.is_blocked:
            abort(401, "User is blocked!")

        g.user = user

        return token
    except JWTError:
        abort(401, "Token broken!")


def basic_auth(email, password, required_scopes=None) -> dict:
    return {"sub": Auth.login(email, password)}


def apikey_auth(token, required_scopes=None) -> dict:
    if token != CDN_SECRET:
        abort(401, "CDN token broken!")
    return {"sub": "CDN"}


def signup() -> Tuple[dict, int]:
    return Auth.signup(connexion.request.json), 201


def login(user) -> Tuple[dict, int]:
    return user, 201


@role_admin_or_user_required
def renew(token_info) -> Tuple[dict, int]:
    return Auth.get_token(token_info["sub"]), 201
