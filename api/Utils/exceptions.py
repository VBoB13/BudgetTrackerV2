class AuthError(Exception):
    """
    Error raised by the api.routers.auth module.
    """


class ControllerError(Exception):
    """
    Error thrown by the api.db.controller module.
    """


class CategoriesError(Exception):
    """
    Error raised by the api.objects.categories module.
    """


class CheckSubError(Exception):
    """
    Error raised by the api.check_subscriptions module.
    """


class IncomesError(Exception):
    """
    Error raised by the api.objects.incomes module.
    """


class StatsError(Exception):
    """
    Error raised by the api.objects.stats module.
    """


class StoresError(Exception):
    """
    Error raised by the api.objects.stores module.
    """


class SubscriptionError(Exception):
    """
    Error raised by the api.objects.subscriptions module.
    """


class TransactionsError(Exception):
    """
    Error raised by the api.objects.transactions module.
    """


class UsersError(Exception):
    """
    Error raised by the api.objects.users module.
    """


class UtilError(Exception):
    """
    Error raised by the api.Utils package.
    """


class CommonUtilError(Exception):
    """
    Error raised by the api.Utils.common module.
    """
