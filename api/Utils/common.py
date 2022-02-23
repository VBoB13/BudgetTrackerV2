from datetime import date, datetime


def str_to_date(s: str) -> date:
    d = datetime.strptime(s, "%Y-%m-%d").date
    return d
