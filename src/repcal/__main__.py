import argparse
from .RepublicanDate import RepublicanDate
from .DecimalTime import DecimalTime
from .RepublicanFormatter import RepublicanFormatter
from .cli_date_parse import *

parser = argparse.ArgumentParser(description='Convert a date and time')
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
