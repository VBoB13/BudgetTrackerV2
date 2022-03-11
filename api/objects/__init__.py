from datetime import date, timedelta
from calendar import monthrange

from ..Utils import TODAY, ONE_DAY


subscription_period_dict = {
    'y': timedelta(days=365),
    'm': timedelta(days=monthrange(TODAY.year, TODAY.month)[1]),
    'w': timedelta(weeks=1),
    'd': ONE_DAY
}
