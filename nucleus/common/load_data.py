from nucleus.controllers.users import User
from nucleus.models.users import Roles

roles = [
    {'name': 'admin', 'description': 'Administration user'},
    {'name': 'user', 'description': 'Regular user'},
]

user_admin = {'username': 'admin', 'password': 'secret', 'role': 'admin'}


def load_init_data() -> bool:
    """Load initial data when the application starts."""
    Roles.bulk_create(roles)
    User.create(user_admin)
    return True
