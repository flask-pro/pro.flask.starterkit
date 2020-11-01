from functools import wraps

from flask import abort
from flask import g


def role_admin_required(fn):
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if g.user.roles.name != "admin":
            abort(401)

        return fn(*args, **kwargs)

    return decorated_function


def role_admin_or_user_required(fn):
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if g.user.roles.name not in ["admin", "user"]:
            abort(401)

        return fn(*args, **kwargs)

    return decorated_function
