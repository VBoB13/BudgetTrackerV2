from fastapi import APIRouter, HTTPException

from ..objects.subscriptions import Subscription, SubscriptionList
from ..typing.models import SubscriptionIn, SubscriptionOut, SubscriptionsOut
from ..db.controller import query_db, ControllerError

router = APIRouter(
    prefix='/subscriptions',
    tags=["subscriptions"],
    dependencies=[],
    responses={404: {"detail": "Not found."}},
)


@router.get("/all", description="Show all the registered subscriptions in the database.", response_model=SubscriptionsOut)
async def get_all_subscriptions():
    sql = Subscription.get_all()
    try:
        subscriptions = SubscriptionList(
            [Subscription(item) for item in query_db(sql)])
    except ControllerError as err:
        raise HTTPException(
            500, "Could not retrieve Transactions from database!") from err
    else:
        df = subscriptions.generate_df()
        print(df)

    return subscriptions.__dict__()


@router.post("/add_subscription", description="Add a single Transaction to the database.")
async def add_subscription(subscription: SubscriptionIn):
    sql = Subscription.add_subscription(
        subscription.name, subscription.s_date, subscription.e_date, subscription.cost, subscription.currency, subscription.auto_resub, subscription.period)
    try:
        query_db(sql, True)
    except ControllerError as err:
        raise HTTPException(
            500, "Could not insert new Subscription ({} - {} to {} ({}{}/{})) into database!".format(
                subscription.name, subscription.s_date, subscription.e_date, subscription.cost, subscription.currency, subscription.period)) from err
    else:
        sql = Subscription.get_subscription_by_name(subscription.name)
        try:
            sub = Subscription(query_db(sql))
        except ControllerError as err:
            raise HTTPException(
                500, "Could not retrieve the newly added Transaction ({}) from database!".format(Transaction.name)) from err
        else:
            return
