from datetime import datetime, date
import json
import os
from traceback import print_tb
from fastapi import APIRouter, HTTPException

from colorama import Fore, Style

from ..objects.transactions import Transaction, TransactionList
from ..typing.models import TransactionIn, TransactionOut, TransactionsOut
from ..db.controller import query_db, ControllerError

router = APIRouter(
    prefix='/transactions',
    tags=["transactions"],
    dependencies=[],
    responses={404: {"detail": "Not found."}},
)


@router.get("/get_all", description="Show all the registered transactions in the database.", response_model=TransactionsOut)
async def get_all_Transactions():
    sql = Transaction.get_all_transactions()
    try:
        transactions = TransactionList(
            [Transaction(item) for item in query_db(sql)])
    except ControllerError as err:
        raise HTTPException(
            500, "Could not retrieve Transactions from database!") from err
    else:
        df = transactions.generate_df()
        print(df)

    return {"transactions": [transaction for transaction in transactions]}


@router.post("/add", description="Add a single Transaction to the database.", response_model=TransactionsOut)
async def add_transaction(transaction: TransactionIn):
    sql = Transaction.add_transaction(
        transaction.date, transaction.amount, transaction.currency, transaction.category, transaction.user_id, transaction.store, transaction.comment)
    try:
        query_db(sql, True)
    except ControllerError as err:
        raise HTTPException(
            500, "Could not insert new Transaction ({} - {} {} ({})) into database!".format(
                transaction.date, transaction.amount, transaction.currency, transaction.category)) from err
    else:
        sql = Transaction.get_transactions_by_date(transaction.date)
        try:
            result_transactions = [dict(Transaction(item))
                                   for item in query_db(sql)]
        except ControllerError as err:
            raise HTTPException(
                500, "Could not retrieve the newly added Transaction ({}) from database!".format(Transaction.name)) from err
        else:
            return {"transactions": result_transactions}


@router.post("/add_temp", description="Add a Transaction to a temporary file that get its content added to DB later on.")
async def add_transaction_temp(transaction: TransactionIn):
    trans = Transaction(
        date=datetime.strptime(transaction.date, "%Y-%m-%d").date(),
        amount=transaction.amount,
        currency=transaction.currency,
        category=transaction.category,
        user=transaction.user_id,
        store=transaction.store,
        comment=transaction.comment
    )
    try:
        pwd = os.getcwd()
        data = {}
        with open(pwd + "/fake_data.json", "r+") as json_file:
            data = json.load(json_file)
            data["transactions"].append(dict(trans))

        with open(pwd + "/fake_data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

    except Exception as err:
        print(Fore.RED, err, Style.RESET_ALL)
        print_tb(err.__traceback__)
    else:
        print(Fore.GREEN, "Success!", Style.RESET_ALL)

    return {
        "transaction": trans
    }
