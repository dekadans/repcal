from datetime import datetime, timedelta, time, date
import re


def get_default_date(paris_mean):
    if paris_mean:
        dt = datetime.utcnow()
        dt += timedelta(minutes=9, seconds=21)
    else:
        dt = datetime.now()

    return dt.date(), dt.time()


def parse_date(datestr):
    is_time_re = re.compile('^[0-9]+:[0-9]+(:[0-9]+)?')
    is_date_re = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    d = t = None

    if is_time_re.match(datestr):
        t = time.fromisoformat(datestr)
    elif is_date_re.match(datestr):
        d = date.fromisoformat(datestr)
    else:
        dt = datetime.fromisoformat(datestr)
        d = dt.date()
        t = dt.time()

    return d, t
