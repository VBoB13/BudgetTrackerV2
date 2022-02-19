class ControllerError(Exception):
    """
    Error thrown by the api.db.controller module.
    """

class UsersError(Exception):
    """
    Error raised by the api.objects.users module.
    """

class AuthError(Exception):
    """
    Error raised by the api.routers.auth module.
    """