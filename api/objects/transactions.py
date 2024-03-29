import os
import json
from colorama import Fore, Style, Back
from typing import Iterator, Tuple, overload
import datetime
import pandas as pd
from pprint import pprint


from ..objects.categories import Category, CategoryList
from ..objects.users import User
from ..objects.stores import Store
from ..Utils.exceptions import TransactionsError, ControllerError, CategoriesError
from ..Utils.common import str_to_date
from ..db.controller import query_db
from . import TODAY, CATEGORY_COLORS


class Transaction(object):
    """
    Reminder: 'date' corresponds to 't_date' in DB.
    """

    def __init__(self, row: Tuple = None, **kwargs):
        self.id: int = None
        self.date: datetime.date = None
        self.amount: float or int = None
        self.currency = None
        self.category: Category = None
        self.user: User = None
        self.store: Store = None
        self.comment: str = None

        if row is not None:
            self.id = int(row[0])
            self.date: datetime.date = row[1] if isinstance(
                row[1], datetime.date) else str_to_date(row[1])
            self.amount = float(row[2])
            self.currency: str = str(row[3])
            self.category: Category = self._fetch_category(row[4])
            self.user: User = self._fetch_user(int(row[5]))
            self.store: Store = self._fetch_store(row[6])
            self.comment: str = row[7] if row[7] else ""

        if kwargs:
            self.id: int = kwargs.pop("id", -1)
            self.date: datetime.date = kwargs.pop("date", None)
            self.amount: float or int = kwargs.pop("amount", None)
            self.currency = kwargs.pop("currency", None)
            self.category: Category = self._fetch_category(
                kwargs.pop("category", None))
            self.user: User = kwargs.pop("user", None)
            self.store: Store = kwargs.pop("store", None)
            self.comment: str = kwargs.pop("comment", None)

    def __str__(self):
        return "{} - {} {}".format(self.date, self.amount, self.currency)

    def __iter__(self):
        if self.id:
            yield "id", self.id
        yield "date", self.date.strftime("%Y-%m-%d") if isinstance(self.date, datetime.date) else self.date
        yield "amount", self.amount
        yield "currency", self.currency
        yield "category", str(self.category)
        yield "user", str(self.user) if isinstance(self.user, User) else int(self.user)
        yield "store", str(self.store)
        yield "comment", self.comment
        # else:
        #     raise TransactionsError(
        #         "Not iterable: no 'id'! id:{} & date:{}".format(self.id, self.date))

    def _fetch_category(self, cat_name: str) -> Category:
        sql = Category.get_category_by_name(cat_name)
        category = None
        try:
            category = Category(query_db(sql))
        except Exception as err:
            print(err)

        if category is not None:
            return category
        return cat_name

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
        if store is not None:
            return store
        return store_id

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
        if user is not None:
            return user
        return user_id

    @staticmethod
    def get_all_transactions():
        return """
            SELECT tra.id, tra.t_date, tra.amount, tra.currency, cat.name, u.id, st.id, tra.comment
            FROM "TRANSACTIONS" AS tra
            JOIN "CATEGORIES" AS cat ON tra.category_id = cat.id
            JOIN "USERS" AS u ON tra.user_id = u.id
            JOIN "STORES" AS st ON tra.store_id = st.id
            WHERE tra.t_date >= date '{}'
            ORDER BY
                tra.t_date DESC,
                tra.user_id ASC,
                st.s_name ASC;
        """.format((TODAY - datetime.timedelta(days=30)).strftime("%Y-%m-%d"))

    def add_transaction_unit(self):
        return """
            INSERT INTO "TRANSACTIONS"
            (t_date, amount, currency, category_id, user_id, store_id, comment)
            VALUES (date '{}', {}, '{}',
                    (SELECT (cat.id) FROM "CATEGORIES" AS cat WHERE cat.name='{}'),
                    {},
                    (SELECT (st.id) FROM "STORES" AS st WHERE s_name='{}'),
                    '{}');
            UPDATE "STASH" SET amount=amount-{} WHERE amount=(SELECT max(amount) FROM "STASH");
        """.format(
            self.date,
            self.amount,
            self.currency,
            self.category,
            self.user,
            self.store,
            self.comment,
            self.amount
        )

    @staticmethod
    def add_transaction(date: str, amount: float, currency: str, category: str, user_id: int, store_name: str, comment: str):
        date_vals = date.split("-")
        if len(date_vals) > 3:
            raise TransactionsError(
                "Got a few too many dashes '-' in the date, don't ya?")
        try:
            new_date = datetime.date(
                year=int(date_vals[0]), month=int(date_vals[1]), day=int(date_vals[2]))
        except Exception as err:
            raise TransactionsError(
                "Could not convert the sent date into datetime.date object!") from err

        # Check whether the category exists.
        # We try to add it if it doesn't
        if not Transaction().check_for_category(category):
            # First, we have to get some new color
            try:
                current_colors = CategoryList.get_all_category_colors()
                for index, color in enumerate(CATEGORY_COLORS):
                    if color not in current_colors:
                        query_db(Category.add_category(category, color), True)
                        category = Category(
                            query_db(Category.get_category_by_name(category))).name
                        break
                    if index == len(CATEGORY_COLORS)-1:
                        raise CategoriesError(
                            "No more colors to choose from!\nAdd more in CATEGORY_COLORS (api.objects.__init__).")

            except CategoriesError as err:
                raise TransactionsError(
                    "Could not get a new color for the new category '{}'!".format(category)) from err
            except Exception as err:
                raise TransactionsError(
                    "Could not save the new category into database!") from err

        return """
            INSERT INTO "TRANSACTIONS"
            (t_date, amount, currency, category_id, user_id, store_id, comment)
            VALUES (date '{}', {}, '{}',
                    (SELECT (cat.id) FROM "CATEGORIES" AS cat WHERE cat.name='{}'),
                    {},
                    (SELECT (st.id) FROM "STORES" AS st WHERE s_name='{}'),
                    '{}');
            UPDATE "STASH" SET amount=amount-{} WHERE amount=(SELECT max(amount) FROM "STASH");
        """.format(new_date.strftime("%Y-%m-%d"), amount, currency, category, user_id, store_name, comment, amount)

    def check_for_category(self, category: str) -> bool:
        category = self._fetch_category(category)
        return isinstance(category, Category)

    def edit(self, old=None):
        if self.id != -1:
            sql = """
                UPDATE "TRANSACTIONS" SET
                    t_date='{}',
                    amount={},
                    currency='{}',
                    category_id={},
                    user_id={},
                    store_id={},
                    comment='{}'
                WHERE id={}
            """.format(
                self.date,
                self.amount,
                self.currency,
                self.category,
                self.user,
                self.store,
                self.comment,
                self.id
            )
            query_db(sql, insert=True)

        else:
            if old is not None:
                pwd = os.getcwd()
                data = {}
                with open(pwd + "/fake_data.json", "r+") as json_file:
                    data = json.load(json_file)
                    data_list = list(data["transactions"])

                    for index, transaction in enumerate(data_list):
                        if dict(transaction) == dict(old):
                            edit_index = index

                    data["transactions"][edit_index] = dict(self)
                    data["transactions"] = sorted(
                        data["transactions"], key=lambda x: x["date"])

                with open(pwd + "/fake_data.json", "w") as json_file:
                    json.dump(data, json_file, indent=4)

            else:
                raise TransactionsError(
                    "Cannot edit a temporarily registered transaction without knowing its old data!")

        print(Fore.YELLOW, "Successfully edited transaction!", Style.RESET_ALL)

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
                if isinstance(transaction, Transaction):
                    self.append(transaction)
                    continue
                raise TransactionsError(
                    "This list can only contain Transactions!")

    def __iter__(self) -> Iterator[Transaction]:
        for transaction in super().__iter__():
            yield transaction
            continue

    def append(self, obj) -> None:
        if isinstance(obj, Transaction):
            return super().append(obj)
        raise TransactionsError(
            "Can't append anyhing other than Transaction instances, not even {}.".format(type(obj).__name__))

    def extend(self, obj):
        if isinstance(obj, self.__class__):
            return super().extend(obj)
        raise TransactionsError(
            "Can't extend any other list than TransactionLists [Transaction], not {}.".format(type(obj).__name__))

    def get_sum(self) -> int:
        transactions_sum = int(0)
        for transaction in self.__iter__():
            transactions_sum += transaction.amount
        return transactions_sum

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

    def delete_all(self) -> None:
        """
        Deletes all transaction objects within the list from DB.
        """
        transaction_ids = []
        temp_transactions = []
        try:
            for transaction in self.__iter__():
                if transaction.id != -1:
                    transaction_ids.append(transaction.id)
                    sql = """
                        DELETE FROM "TRANSACTIONS" WHERE id IN ({});
                    """.format(','.join(id_no for id_no in transaction_ids))
                else:
                    temp_transactions.append(transaction)
            if len(transaction_ids) > 0:
                query_db(sql, delete=True)
            if len(temp_transactions) > 0:
                pwd = os.getcwd()
                data = {}

                with open(pwd + "/fake_data.json", "r") as json_file:
                    data = json.load(json_file)

                for transaction in temp_transactions:
                    if dict(transaction) in data["transactions"]:
                        try:
                            data["transactions"].remove(dict(transaction))
                        except Exception:
                            continue

        except Exception as err:
            raise TransactionsError(
                "DELETE TRANSACTIONS: Couldn't parse through transactions' IDs!") from err
        else:
            with open(pwd + "/fake_data.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
            print(Fore.YELLOW, "Deleted", Fore.RED, len(transaction_ids),
                  Fore.YELLOW, "transactions from DB.", Style.RESET_ALL)
            print(Fore.YELLOW, "Deleted", Back.LIGHTYELLOW_EX, Fore.LIGHTRED_EX, len(
                temp_transactions), Style.RESET_ALL, Fore.YELLOW, "transactions from temporary file.")

    def generate_df(self):
        index, cols, data = self._generate_col_data()
        try:
            return pd.DataFrame(data, columns=cols, index=index)
        except Exception as err:
            raise TransactionsError(
                "Could not convert Transactions into DF!") from err
