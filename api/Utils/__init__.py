from calendar import monthrange
from datetime import date, timedelta

TODAY = date.today()
START_DAY = date(year=2022, month=2, day=22)
ONE_DAY = timedelta(days=1)
ONE_MONTH = timedelta(days=monthrange(TODAY.year, TODAY.month)[1])
ONE_YEAR = timedelta(days=365)
ONE_MONTH_AHEAD = TODAY + \
    timedelta(days=monthrange(TODAY.year, TODAY.month)[1])
ONE_MONTH_AGO = TODAY - timedelta(days=monthrange(TODAY.year, TODAY.month)[1])

# TODO:
# Make sure to fetch the exchange rates so that
# it can easily be utilized by Transaction.add_transaction.
USD_NTD = None
