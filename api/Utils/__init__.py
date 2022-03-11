from calendar import monthrange
from datetime import date, timedelta

TODAY = date.today()
START_DAY = date(year=2022, month=2, day=22)
ONE_DAY = timedelta(days=1)
ONE_MONTH_AHEAD = TODAY + \
    timedelta(days=monthrange(TODAY.year, TODAY.month)[1])
ONE_MONTH_AGO = TODAY - timedelta(days=monthrange(TODAY.year, TODAY.month)[1])
