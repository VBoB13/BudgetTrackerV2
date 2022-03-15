import os
import requests
import bs4
from colorama import Fore, Style
from pprint import pprint
from datetime import date, datetime

from .exceptions import CommonUtilError
from ..db.controller import query_db

EXCHANGE_KEY = os.environ["EXCH_KEY"]
EXCH_BASE_URL = "http://data.fixer.io/api/"


def str_to_date(s: str) -> date:
    d = datetime.strptime(s, "%Y-%m-%d").date
    return d


def get_ntd_rates(date_obj: date) -> float:
    return


def save_rate():
    date_str = input("Enter date: ")
    if date_str == "":
        date_str = date.today().strftime("%Y-%m-%d")
        print("Using date:", Fore.YELLOW, date_str, Style.RESET_ALL)
    base = input("Enter BASE currency: ")
    target = input("Enter TARGET currency: ")
    rate = float(input("Enter rate: "))

    sql = """
        INSERT INTO "EXCHANGE_RATES" (base, target, rate, r_date)
        VALUES('{}', '{}', {}, '{}')
    """.format(base, target, rate, date_str)

    try:
        result = query_db(sql, True)
    except Exception as err:
        print(Fore.RED, err, Style.RESET_ALL)
        raise CommonUtilError("Could not save exchange rate into DB!") from err

    if result:
        print(Fore.GREEN, "Successfully saved: {} to {}: {}".format(
            base, target, rate))


if __name__ == '__main__':
    # today = date.today()
    # get_ntd_rates(today)
    save_rate()
