import os
from colorama import Fore, Style
from datetime import date, datetime

from .exceptions import CommonUtilError, ControllerError
from ..db.controller import query_db


def str_to_date(s: str) -> date:
    d = datetime.strptime(s, "%Y-%m-%d").date
    return d


def get_ntd_from_base_date(base: str, date_obj: date) -> float:
    sql = """
        SELECT rate FROM "EXCHANGE_RATES"
        WHERE r_date <=date '{}'
        AND base='{}'
        ORDER BY r_date DESC
        LIMIT 1
    """.format(date_obj.strftime("%Y-%m-%d"), base)
    try:
        rate = query_db(sql)[0][0]
    except ControllerError as err:
        raise CommonUtilError("Could not get NTD rate from DB.\nBase: {}\nDate: {}".format(
            base, date_obj.strftime("%Y-%m-%d")))
    return rate


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
    today = date.today()
    print("USD - NTD:", get_ntd_from_base_date("USD", today))
    # save_rate()
