class ControllerError(Exception):
    """
    Error thrown by the api.db.controller module.
    """


class UsersError(Exception):
    """
    Error raised by the api.objects.users module.
    """


class CategoriesError(Exception):
    """
    Error raised by the api.objects.categories module.
    """


class StoresError(Exception):
    """
    Error raised by the api.objects.stores module.
    """


class TransactionsError(Exception):
    """
    Error raised by the api.objects.transactions module.
    """


class AuthError(Exception):
    """
    Error raised by the api.routers.auth module.
    """
