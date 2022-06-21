from datetime import datetime, date
import json
import os
from pprint import pprint
from traceback import print_tb
from fastapi import APIRouter, HTTPException

from colorama import Back, Fore, Style

from ..objects.transactions import Transaction, TransactionList
from ..typing.models import TransactionIn, TransactionOut, TransactionsOut, TransactionsIn
from ..db.controller import query_db, ControllerError

router = APIRouter(
    prefix='/transactions',
    tags=["transactions"],
    dependencies=[],
    responses={404: {"detail": "Not found."}},
)


@router.get("/get_all", description="Show all the registered transactions in the database.")
async def get_all_transactions():
    sql = Transaction.get_all_transactions()
    try:
        transactions = TransactionList(
            [Transaction(item) for item in query_db(sql)])
        trans_sum = transactions.get_sum()
    except ControllerError as err:
        try:
            pwd = os.getcwd()
            data = {}

            with open(pwd + "/fake_data.json", "r") as json_file:
                data = json.load(json_file)

            transactions = TransactionList(
                [Transaction(**item) for item in data["transactions"]])

            trans_sum = transactions.get_sum()

            if trans_sum > 10000:
                print(Back.RED, Fore.BLACK,
                      "More than $10000 worth of transactions in temp!", Style.RESET_ALL)
                print("Sum:", trans_sum)

            return {
                "transactions": transactions,
                "sum": trans_sum,
                "temp": True
            }
        except Exception:
            raise HTTPException(
                500, "Could not retrieve Transactions from database!") from err
    else:
        df = transactions.generate_df()
        print(df)

    return {
        "transactions": transactions,
        "sum": trans_sum,
        "temp": False
    }


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
            data["transactions"] = sorted(
                data["transactions"], key=lambda x: x["date"])

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


@router.post("/temp_to_db", description="Endpoint to initiate the transferral of the temporarily registered transactions.")
async def temp_to_db():
    try:
        pwd = os.getcwd()
        data = {}

        def transaction_gen(trans_data: dict):
            for transaction in trans_data["transactions"]:
                yield Transaction(**transaction)

        with open(pwd + "/fake_data.json", "r") as json_file:
            data = json.load(json_file)

        for transaction in transaction_gen(data):
            # query_db(transaction.add_transaction(), insert=True)
            print(transaction)

    except Exception as err:
        print(Fore.RED, err, Style.RESET_ALL)
        print_tb(err.__traceback__)
        raise HTTPException(500, detail=str(err))


@router.get("/check_temp_to_db", description="This endpoint returns the amount of transactions that are awaiting to be transferred from file to DB.")
async def check_temp_to_db():
    try:
        pwd = os.getcwd()
        data = {}

        with open(pwd + "/fake_data.json", "r") as json_file:
            data = json.load(json_file)

        return {
            "transactions": len(data["transactions"])
        }
    except Exception as err:
        print(err)
        print_tb(err.__traceback__)
        raise HTTPException(500, detail=str(err))


@router.post("/delete", description="Delete as many transactions as you want by sending all transaction you want deleted to this endpoint.")
async def delete_transactions(transactions: TransactionsIn):
    try:
        pprint(transactions.transactions)
        transaction_list = TransactionList(
            [Transaction(**{
                "id": transaction.id,
                "date": transaction.date,
                "amount": transaction.amount,
                "currency": transaction.currency,
                "category": transaction.category,
                "user": transaction.user,
                "store": transaction.store,
                "comment": transaction.comment
            }) for transaction in transactions.transactions])
        transaction_list.delete_all()
    except Exception as err:
        raise HTTPException(status_code=500, detail="Could not delete all the transactions! Reason:" + str(
            err)+"\n"+print_tb(err.__traceback__))


if __name__ == "__main__":
    try:
        pwd = os.getcwd()
        data = {}

        def transaction_gen(trans_data: dict):
            for transaction in trans_data["transactions"]:
                yield Transaction(**transaction)

        with open(pwd + "/fake_data.json", "r") as json_file:
            data = json.load(json_file)

        if len(data["transactions"]) > 0:
            for transaction in transaction_gen(data):
                query_db(transaction.add_transaction_unit(), insert=True)
        else:
            raise Exception("No temp. data to transfer!")

    except Exception as err:
        print(Fore.RED, err, Style.RESET_ALL)
        print_tb(err.__traceback__)

    else:
        data.clear()
        data["transactions"] = []
        try:
            with open(pwd + "/fake_data.json", "w") as json_file:
                json_file.write(json.dump(data))
        except Exception as err:
            print(Fore.RED, "Unable to clear fake_data.json of data!", Style.RESET_ALL)
            print(err)
            print_tb(err.__traceback__)
        else:
            print(Fore.GREEN, "SUCCESS!", Style.RESET_ALL)
