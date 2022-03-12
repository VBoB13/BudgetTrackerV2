from colorama import Fore, Style
from typing import Tuple, Iterator
from calendar import monthrange
from datetime import date
import pandas as pd
import re
from traceback import print_tb

from ..Utils.exceptions import SubscriptionError
from ..Utils.common import str_to_date
from ..db.controller import query_db
from .transactions import Transaction, TransactionList

from . import subscription_period_dict
from ..Utils import TODAY, ONE_DAY, ONE_MONTH, ONE_YEAR


class Subscription(object):
    """
    Reminder: 'date' corresponds to 't_date' in DB.
    """

    def __init__(self, row: Tuple = None, **kwargs):
        self.id = None
        self.name = None
        self.start_date = None
        self.end_date = None
        self.cost = None
        self.currency = None
        self.auto_resub = None
        self.period = None

        if row is not None:
            self.id = int(row[0])
            self.name = str(row[1])
            self.start_date = row[2] if isinstance(
                row[2], date) else str_to_date(row[2])
            self.end_date = row[3] if isinstance(
                row[3], date) else str_to_date(row[3])
            self.cost = str(row[4])
            self.currency = str(row[5])
            self.auto_resub = row[6]
            self.period = self._fetch_timeperiod(row[7])
        if kwargs:
            self.id = kwargs.pop("id")
            self.name = kwargs.pop("name")
            self.start_date = str_to_date(kwargs.pop("start_date"))
            self.end_date = str_to_date(kwargs.pop("end_date"))
            self.cost = kwargs.pop("cost")
            self.currency = kwargs.pop("currency")
            self.auto_resub = kwargs.pop("auto_resub")
            re_match = re.match(
                "^(?P<amount>[1-9]{1,2}) (?P<unit>days)$", kwargs.pop("period"))
            self.period = self._fetch_timeperiod(
                re_match.group("amount")+re_match.group("unit")[0])

    def __str__(self):
        if self.id:
            return "{}: {} {}/{}".format(self.name, self.cost, self.currency, str(self.period).split(", ")[0])
        return "No real subscription.(No id detected.)"

    def __iter__(self):
        if self.id:
            yield "id", self.id
            yield "name", self.name
            yield "start_date", self.start_date.strftime("%Y-%m-%d")
            yield "end_date", self.end_date.strftime("%Y-%m-%d")
            yield "cost", self.cost
            yield "currency", self.currency
            yield "auto_resub", "Y" if self.auto_resub else "N"
            yield "period", str(self.period).split(", ")[0]
        else:
            raise Exception(
                "Not iterable: no 'id'! id:{} & name:{}".format(self.id, self.name))

    def _fetch_timeperiod(self, timedelta: str):
        """
        Takes strings that represent simple timedelta-data.
        n[unit] =>  '2y' is 2 years
                    '1m' is 1 month
                    '3w' is 3 weeks
                    '5d' is 5 days
        """
        re_match = re.match("^(?P<amount>[1-9])(?P<unit>[ymwd])$", timedelta)
        if re_match:
            return subscription_period_dict[re_match.group('unit')] * int(re_match.group('amount'))
        raise SubscriptionError(
            "Could not decipher the subscription period string!")

    def check_sub_transactions(self):
        sql = """
            SELECT * FROM "TRANSACTIONS" WHERE amount={} AND currency='{}' AND comment='{}' AND t_date <= CURRENT_DATE
        """.format(self.cost, self.currency, self.name, TODAY.strftime("%Y-%m-%d"))
        try:
            results = query_db(sql)
        except Exception as err:
            raise SubscriptionError(
                "Could not fetch Transactions from database!") from err
        compare_date = self.start_date
        if self.period is None:
            raise SubscriptionError(
                "Cannot iterate through dates when no period is set!" + Fore.RED + "\n -- self.period: {}".format(
                    str(self.period) if self.period is not None else None) + Style.RESET_ALL)
        date_list = []
        if self.end_date < TODAY:
            while compare_date <= self.end_date:
                date_list.append(compare_date)
                if self.period == ONE_MONTH:
                    compare_date += ONE_DAY * \
                        monthrange(compare_date.year, compare_date.month)[1]
                if self.period == ONE_YEAR:
                    compare_date += self.period
        else:
            while compare_date <= TODAY:
                date_list.append(compare_date)
                if self.period == ONE_MONTH:
                    compare_date += ONE_DAY * \
                        monthrange(compare_date.year, compare_date.month)[1]
                if self.period == ONE_YEAR:
                    compare_date += self.period

        if len(results) != len(date_list):
            trans_list = TransactionList(
                [Transaction(trans_data) for trans_data in results])
            trans_date_list = []
            for transaction in trans_list:
                trans_date_list.append(transaction.date)
            for date_obj in date_list:
                try:
                    if date_obj not in trans_date_list and date_obj < self.end_date:
                        sql_query = Transaction.add_transaction(
                            date_obj.strftime("%Y-%m-%d"),
                            self.cost,
                            self.currency,
                            "Others",
                            1,
                            "Other",
                            self.name
                        )
                        query_db(sql_query, True)
                        print(self, "Added transaction for", Fore.YELLOW,
                              date_obj.strftime("%Y-%m-%d"), Style.RESET_ALL)
                        continue
                except Exception as err:
                    print(Fore.RED, "--- !WARNING! ---", Style.RESET_ALL)
                    print(err)
                    print_tb(err.__traceback__)

        else:
            print(self, Fore.GREEN, "Updated!", Style.RESET_ALL)

    @ staticmethod
    def add_subscription(name: str, s_date: date, e_date: date,
                         cost: float, currency: str, auto_resub: bool, period: str):
        """
            Method that produces the SQL which inserts a new Subscription into the DB.
        """

        sql = """
            INSERT INTO "SUBSCRIPTIONS"
            (name, start_date, end_date, cost, currency, auto_resub, period)
            VALUES ('{}', date '{}', date '{}', {}, '{}', {}, '{}')
        """
        return sql.format(name, s_date, e_date, cost, currency, auto_resub, period)

    @ staticmethod
    def get_all():
        """
        Method that returns the SQL which gets all Subscriptions from the DB.
        """

        sql = """
            SELECT id, name, start_date, end_date, cost, currency, auto_resub, period FROM "SUBSCRIPTIONS"
            ORDER BY start_date DESC
        """
        return sql

    @ staticmethod
    def get_subscription_by_name(name: str):
        """
        Method that returns the SQL which gets a Subscription from DB by name.
        """
        sql = """
            SELECT id, name, start_date, end_date, cost, currency, auto_resub, period FROM "SUBSCRIPTIONS"
            WHERE name='{}'
        """
        return sql.format(name)

    @ staticmethod
    def get_non_expired_subs():
        """
        Method that returns SQL which gets all subscriptions that have not yet
        expired OR have auto_resub == true.
        """
        sql = """
            SELECT id, name, start_date, end_date, cost, currency, auto_resub, period FROM "SUBSCRIPTIONS" WHERE end_date < CURRENT_DATE OR auto_resub=true;
        """
        return sql


class SubscriptionList(list):
    def __init__(self, trans_list: list = None):
        super().__init__()
        self.id = []
        self.name = []
        self.start_date = []
        self.end_date = []
        self.cost = []
        self.currency = []
        self.auto_resub = []
        self.period = []

        if trans_list:
            for subscription in trans_list:
                self.append(subscription)

    def __dict__(self):
        return {"subscriptions": [sub for sub in self.__iter__()]}

    def __iter__(self) -> Iterator[Subscription]:
        for index in range(len(self)):
            if isinstance(self[index], Subscription):
                yield self[index]
                continue
            raise SubscriptionError("Item is not a Subscription instance!")

    def append(self, obj) -> None:
        if isinstance(obj, Subscription):
            return super().append(obj)
        raise SubscriptionError(
            "Can't append anyhing other than Subscription instances, not even {}.".format(type(obj).__name__))

    def extend(self, obj):
        if isinstance(obj, self.__class__):
            return super().extend(obj)
        raise SubscriptionError(
            "Can't extend any other list than SubscriptionLists [Subscription], not {}.".format(type(obj).__name__))

    def _generate_col_data(self):
        index = []
        cols = ["name", "s_date", "e_date",
                "cost", "currency", "auto_resub", "period"]
        data = []
        for tr in self.__iter__():
            index.append(tr.id)
            data.append([tr.name, tr.start_date.strftime("%Y-%m-%d"), tr.end_date.strftime(
                "%Y-%m-%d"), tr.cost, tr.currency, tr.auto_resub, tr.period])

        return index, cols, data

    def generate_df(self):
        index, cols, data = self._generate_col_data()
        try:
            return pd.DataFrame(data, columns=cols, index=index)
        except Exception as err:
            raise SubscriptionError(
                "Could not convert Subscriptions into DF!") from err

    def check_sub_transactions(self):
        for sub in self.__iter__():
            sub.check_sub_transactions()
