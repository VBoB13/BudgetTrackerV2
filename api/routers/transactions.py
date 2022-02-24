from fastapi import APIRouter, HTTPException

from ..objects.transactions import Transaction
from ..typing.models import TransactionIn, TransactionOut, TransactionsOut
from ..db.controller import query_db, ControllerError

router = APIRouter(
    prefix='/transactions',
    tags=["transactions"],
    dependencies=[],
    responses={404: {"detail": "Not found."}},
)


@router.get("/all", description="Show all the registered transactions in the database.", response_model=TransactionsOut)
async def get_all_Transactions():
    sql = Transaction.get_all_transactions()
    try:
        transactions = [dict(Transaction(item)) for item in query_db(sql)]
    except ControllerError as err:
        raise HTTPException(
            500, "Could not retrieve Transactions from database!") from err

    return {"transactions": transactions}


@router.post("/add_Transaction", description="Add a single Transaction to the database.", response_model=TransactionsOut)
async def add_Transaction(transaction: TransactionIn):
    sql = Transaction.add_transaction(
        transaction.date, transaction.amount, transaction.currency, transaction.category, transaction.user_id, transaction.store)
    try:
        query_db(sql, True)
    except ControllerError as err:
        raise HTTPException(
            500, "Could not insert new Transaction ({} - {} {} ({})) into database!".format(
                transaction.date, transaction.amount, transaction.currency, transaction.category)) from err
    else:
        sql = Transaction.get_transactions_by_date(transaction.date)
        try:
            result_Transactions = [dict(Transaction(item))
                                   for item in query_db(sql)]
        except ControllerError as err:
            raise HTTPException(
                500, "Could not retrieve the newly added Transaction ({}) from database!".format(Transaction.name)) from err
        else:
            return {"transactions": result_Transactions}
