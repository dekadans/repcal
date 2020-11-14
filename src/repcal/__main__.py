import argparse
from .RepublicanDate import RepublicanDate
from .DecimalTime import DecimalTime
from .RepublicanFormatter import RepublicanFormatter
from .cli_date_parse import *

parser = argparse.ArgumentParser(description='Convert a date and time')
parser.add_argument('date', help='The datetime ISO string to convert, defaults to current UTC', nargs='?')
parser.add_argument('--format', help='A datetime format string')
parser.add_argument('--paris-mean', action='store_true')

args = parser.parse_args()

default_format = []
rdate = dtime = None

if args.date is not None:
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
