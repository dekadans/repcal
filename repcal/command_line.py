import argparse
from .RepublicanDate import RepublicanDate
from .DecimalTime import DecimalTime
from .RepublicanFormatter import RepublicanFormatter
from datetime import datetime, timedelta, time, date
import re


def main():
    parser = argparse.ArgumentParser(description='Converts and prints date and time in the French Republican style.')
    parser.add_argument('date', help='The datetime ISO string to convert, defaults to current local time. May be full datetime or just date or time.', nargs='?')
    parser.add_argument('--format', help='A format definition string')
    parser.add_argument('--paris-mean', action='store_true', help='Changes default date from local time to Paris Mean Time.')

    args = parser.parse_args()

    default_format = []
    rdate = dtime = None

    if args.date is not None:
        if args.paris_mean:
            print('Paris Mean Time is only available as a default date option')
            exit()
        d, t = parse_date(args.date)
    else:
        d, t = get_default_date(args.paris_mean)

    if t is not None:
        dtime = DecimalTime.from_standard_time(t)
        default_format.append(DecimalTime.default_formatting)
    if d is not None:
        rdate = RepublicanDate.from_gregorian(d)
        default_format.append(RepublicanDate.default_formatting)

    default_format = ', '.join(default_format)

    formatter = RepublicanFormatter(rdate=rdate, dtime=dtime)
    print(formatter.format(args.format or default_format))


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
