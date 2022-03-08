from datetime import date, timedelta
from typing import List, Tuple
from pprint import pprint

from ..Utils.exceptions import IncomesError
from .users import User
from ..db.controller import query_db, ControllerError


class Income(object):
    def __init__(self, row=None):
        self.id = None
        self.user = None
        self.amount = None
        self.currency = None
        self.date = None

        if row:
            self.id = row[0]
            self.user = self._get_user(row[1])
            self.amount: float = row[2]
            self.currency = row[3]
            self.date: date = row[4]

    def __str__(self):
        return "+${} ({}/{})".format(self.amount, self.date.strftime("%Y-%m-%d"), self.user.name)

    def __iter__(self):
        yield "id", self.id
        yield "user", str(self.user)
        yield "amount", self.amount
        yield "currency", self.currency
        yield "date", self.date.strftime("%Y-%m-%d")

    def _get_user(self, user_id: int):
        sql = User.get_user_by_id(user_id)
        result = query_db(sql)
        return User(result[0])

    @staticmethod
    def get_all_incomes():
        return """
            SELECT * FROM "INCOMES";
        """

    @staticmethod
    def add_income(user_id: int, amount: float, currency: str, date: str):
        return """
            INSERT INTO "INCOMES" (user_id, amount, currency, i_date) VALUES ({}, {}, '{}', date '{}');
            UPDATE "STASH" SET amount=amount+{} WHERE user_id={} AND currency='{}';
        """.format(user_id, amount, currency, date, amount, user_id, currency)
