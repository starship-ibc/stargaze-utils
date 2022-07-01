from datetime import datetime
from decimal import Decimal

EPOCH = datetime.utcfromtimestamp(0)
DATETIME_FMT = "%a %m-%d %I:%M %p"
MARKET_CONTRACT = "stars1fvhcnyddukcqfnt7nlwv3thm5we22lyxyxylr9h77cvgkcn43xfsvgv0pl"


def timestamp_from_str(ts):
    """Returns a timestamp with milliseconds as a datetime timestamp."""
    return datetime.utcfromtimestamp(float(Decimal(ts) / 1000000000))
