from datetime import datetime, timedelta
import argparse
from .RepublicanDate import RepublicanDate
from .DecimalTime import DecimalTime
from .RepublicanFormatter import RepublicanFormatter

default_formatting = DecimalTime.default_formatting + ', ' + RepublicanDate.default_formatting

parser = argparse.ArgumentParser(description='Convert a date and time')
parser.add_argument('date', help='The datetime ISO string to convert, defaults to current UTC', nargs='?')
parser.add_argument('--format', default=default_formatting, help='A datetime format string')

args = parser.parse_args()

if args.date is None:
    t = datetime.utcnow()
else:
    t = datetime.fromisoformat(args.date)

dtime = DecimalTime.from_standard_time(t.time())

if dtime.date_turnover:
    t += timedelta(days=1)

rdate = RepublicanDate.from_gregorian(t.date())

formatter = RepublicanFormatter(rdate=rdate, dtime=dtime)
format_string = args.format

print(formatter.format(format_string))
