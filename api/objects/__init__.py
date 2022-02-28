from datetime import date, timedelta
from calendar import monthrange

today = date.today()

subscription_period_dict = {
    'y': timedelta(days=365),
    'm': timedelta(days=monthrange(today.year, today.month)[1]),
    'w': timedelta(weeks=1),
    'd': timedelta(days=1)
}
