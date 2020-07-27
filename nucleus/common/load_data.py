from nucleus.models.users import Roles

roles = [
    {'name': 'admin', 'description': 'Administration user'},
    {'name': 'user', 'description': 'Regular user'},
]


def load_init_data():
    """Load initial data when the application starts."""
    return Roles.bulk_create(roles)
