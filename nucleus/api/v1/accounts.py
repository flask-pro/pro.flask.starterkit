from nucleus.common.decorators import role_admin_or_user_required
from nucleus.controllers.accounts import Account


@role_admin_or_user_required
def get_profile(token_info) -> dict:
    return Account.get_profile(token_info["sub"]).to_dict()
