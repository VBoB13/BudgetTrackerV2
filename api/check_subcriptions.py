# This module is meant to be run as a separate process, supposedly through the
# frequently used 'api.main' module.
from .db.controller import query_db
from .objects.subscriptions import Subscription, SubscriptionList
from .Utils.exceptions import CheckSubError

# Step 1:
# Check what supscriptions exist that have:
#   -1: Not yet expired
#       OR
#   -2: auto_resub=true


def check_subs():
    sql = Subscription.get_non_expired_subs()
    try:
        results = query_db(sql)
    except Exception as err:
        raise CheckSubError(
            "Could not fetch subscriptions from database!") from err

    sub_list = SubscriptionList([Subscription(item) for item in results])
    sub_list.check_sub_transactions()


if __name__ == '__main__':
    check_subs()
