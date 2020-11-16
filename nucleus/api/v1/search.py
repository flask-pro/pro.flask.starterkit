import connexion

from nucleus.common.decorators import role_admin_or_user_required
from nucleus.common.decorators import role_admin_required
from nucleus.controllers.search import Search


@role_admin_or_user_required
def get_search_list() -> dict:
    return Search.results_list(connexion.request.args)


@role_admin_required
def search_reindex() -> str:
    return Search.reindex(connexion.request.args)
