from datetime import datetime
import argparse
from .RepublicanDate import RepublicanDate
from .DecimalTime import DecimalTime
from .RepublicanFormatter import RepublicanFormatter
from .paris_mean import paris_mean

default_formatting = DecimalTime.default_formatting + ', ' + RepublicanDate.default_formatting

parser = argparse.ArgumentParser(description='Convert a date and time')
parser.add_argument('date', help='The datetime ISO string to convert, defaults to current UTC', nargs='?')
parser.add_argument('--format', default=default_formatting, help='A datetime format string')

args = parser.parse_args()

if args.date is None:
    t = datetime.utcnow()
else:
    t = datetime.fromisoformat(args.date)

rdate, dtime = paris_mean(t)

formatter = RepublicanFormatter(rdate=rdate, dtime=dtime)
print(formatter.format(args.format))
