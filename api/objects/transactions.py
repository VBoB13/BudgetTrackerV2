from pprint import pprint
from typing import Tuple
from datetime import date
import json
import pandas as pd


from ..objects.categories import Category
from ..objects.users import User
from ..objects.stores import Store
from ..Utils.exceptions import TransactionsError, ControllerError, CategoriesError
from ..Utils.common import str_to_date
from ..db.controller import query_db


class Transaction(object):
    """
    Reminder: 'date' corresponds to 't_date' in DB.
    """

    def __init__(self, row: Tuple = None):
        self.id = None
        self.date = None
        self.amount = None
        self.currency = None
        self.category = None
        self.user = None
        self.store = None
        self.comment = None

        if row is not None:
            self.id = int(row[0])
            self.date = row[1] if isinstance(
                row[1], date) else str_to_date(row[1])
            self.amount = float(row[2])
            self.currency = str(row[3])
            self.category = self._fetch_category(row[4])
            self.user = self._fetch_user(int(row[5]))
            self.store = self._fetch_store(row[6])
            self.comment = row[7] if row[7] else ""

    def __str__(self):
        if self.id:
            return "{} - {} {}".format(self.date, self.amount, self.currency)
        return "No real transaction.(No id detected.)"

    def __iter__(self):
        if self.id:
            yield "id", self.id
            yield "date", self.date.strftime("%Y-%m-%d")
            yield "amount", self.amount
            yield "currency", self.currency
            yield "category", str(self.category)
            yield "user", str(self.user)
            yield "store", str(self.store)
            yield "comment", self.comment
        else:
            raise TransactionsError(
                "Not iterable: no 'id'! id:{} & date:{}".format(self.id, self.date))

    def _fetch_category(self, cat_name: str) -> Category:
        sql = Category.get_category_by_name(cat_name)
        category = None
        try:
            category = Category(query_db(sql)[0])
        except ControllerError as err:
            raise TransactionsError(
                "Could not retrieve category data from database!") from err
        except CategoriesError as err:
            raise TransactionsError(
                "Could not convert category data into Category object!") from err

        return category

    def _fetch_store(self, store_id: int) -> User:
        sql = Store.get_store_by_id(store_id)
        store = None
        try:
            store = Store(query_db(sql)[0])
        except ControllerError as err:
            raise TransactionsError(
                "Could not retrieve user data from database!") from err
        except CategoriesError as err:
            raise TransactionsError(
                "Could not convert user data into user object!") from err

        return store

    def _fetch_user(self, user_id: int) -> User:
        sql = User.get_user_by_id(user_id)
        user = None
        try:
            user = User(query_db(sql)[0])
        except ControllerError as err:
            raise TransactionsError(
                "Could not retrieve user data from database!") from err
        except CategoriesError as err:
            raise TransactionsError(
                "Could not convert user data into user object!") from err

        return user

    @staticmethod
    def get_all_transactions():
        return """
            SELECT tra.id, tra.t_date, tra.amount, tra.currency, cat.name, u.id, st.id, tra.comment
            FROM "TRANSACTIONS" AS tra
            JOIN "CATEGORIES" AS cat ON tra.category_id = cat.id
            JOIN "USERS" AS u ON tra.user_id = u.id
            JOIN "STORES" AS st ON tra.store_id = st.id
            ORDER BY
                tra.t_date DESC,
                tra.user_id ASC,
                st.s_name ASC;
        """

    @staticmethod
    def add_transaction(date: str, amount: float, currency: str, category: str, user_id: int, store_name: str, comment: str):
        return """
            INSERT INTO "TRANSACTIONS"
            (t_date, amount, currency, category_id, user_id, store_id, comment)
            VALUES (date '{}', {}, '{}',
                    (SELECT (cat.id) FROM "CATEGORIES" AS cat WHERE cat.name='{}'),
                    {},
                    (SELECT (st.id) FROM "STORES" AS st WHERE s_name='{}'))
        """.format(date, amount, currency, category, user_id, store_name)

    @staticmethod
    def get_transactions_by_date(date: str):
        return """
            SELECT tra.id, tra.t_date, tra.amount, tra.currency, cat.name, u.id, st.id, tra.comment
            FROM "TRANSACTIONS" AS tra
            JOIN "CATEGORIES" AS cat ON tra.category_id = cat.id
            JOIN "USERS" AS u ON tra.user_id = u.id
            JOIN "STORES" AS st ON tra.store_id = st.id
            WHERE tra.t_date = date '{}'
            ORDER BY
                t_date DESC,
                u.id ASC,
                tra.id ASC;
        """.format(date)


class TransactionList(list):
    def __init__(self, trans_list: list = None):
        super().__init__()
        self.id = []
        self.date = []
        self.amount = []
        self.currency = []
        self.category = []
        self.user = []
        self.store = []
        self.comment = []

        if trans_list:
            for transaction in trans_list:
                self.append(transaction)

    def __iter__(self):
        for transaction in super().__iter__():
            if isinstance(transaction, Transaction):
                yield transaction
                continue
            raise TransactionsError("Item is not a Transaction instance!")

    def append(self, obj) -> None:
        if isinstance(obj, Transaction):
            return super().append(obj)
        raise TransactionsError(
            "Can't append anyhing other than Transaction instances!")

    def extend(self, obj):
        if isinstance(obj, self.__class__):
            return super().extend(obj)
        raise TransactionsError(
            "Can't extend any other list than [Transactions] lists.")

    def _generate_col_data(self):
        index = []
        cols = ["date", "amount", "currency",
                "category", "user", "store", "comment"]
        data = []
        for tr in self.__iter__():
            index.append(tr.id)
            data.append([tr.date, tr.amount, tr.currency, str(
                tr.category), str(tr.user), str(tr.store), tr.comment])

        return index, cols, data

    def generate_df(self):
        index, cols, data = self._generate_col_data()
        return pd.DataFrame(data, columns=cols, index=index)
