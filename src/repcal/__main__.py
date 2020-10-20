from datetime import datetime
import argparse
from .RepublicanDate import RepublicanDate
from .DecimalTime import DecimalTime


parser = argparse.ArgumentParser(description='Convert a date and time')
parser.add_argument('date', help='The date to convert', nargs='?')

args = parser.parse_args()

if args.date == None:
    t = datetime.utcnow()
else:
    t = datetime.fromisoformat(args.date)


dtime = DecimalTime.from_standard_time(t.time())
rdate = RepublicanDate.from_gregorian(t.date())

print('{}, {}'.format(
    dtime,
    rdate
))
