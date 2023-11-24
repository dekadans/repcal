import argparse
from .RepublicanDate import RepublicanDate
from .DecimalTime import DecimalTime
from .RepublicanFormatter import RepublicanFormatter
from datetime import datetime, timedelta, time, date, timezone
import re
import logging


class RepcalConsoleException(Exception):
    pass


def main():
    logging.basicConfig(format='%(levelname)s: %(message)s')
    parser = argparse.ArgumentParser(description='Converts and prints date and time in the French Republican style.')
    parser.add_argument('date', help='The ISO date and/or time to convert. Uses current local time is omitted.', nargs='?')
    parser.add_argument('--decimal', action='store_true', help='Represent time as a decimal number.')
    parser.add_argument('--format', help='Explicitly set the output format.')
    parser.add_argument('--paris-mean', action='store_true', help='Use Paris Mean Time as offset (6.49 decimal minutes ahead of UTC).')
    parser.add_argument('--offset', help='Override the local timezone with an offset in minutes from UTC.', type=int)
    args = parser.parse_args()

    if args.decimal:
        DecimalTime.default_formatting = '{%D}'

    try:
        validate_args(args)
        if args.date is not None:
            d, t = parse_date(args.date)
        else:
            d, t = get_default_date(args)

        result = convert(d, t, args.format)
    except RepcalConsoleException as e:
        logging.error(e)
        exit(1)

    print(result)


def validate_args(args):
    if args.date is not None:
        if args.paris_mean or args.offset:
            raise RepcalConsoleException(
                "Setting the UTC offset (using --offset or --paris-mean) "
                "can not be used with an explicit datetime input."
            )
    else:
        if args.paris_mean and args.offset:
            raise RepcalConsoleException('--paris-mean and --offset are mutually exclusive.')
        if args.offset is not None and not (-1440 < args.offset < 1440):
            raise RepcalConsoleException('The --offset must be within 24 hours from UTC.')


def parse_date(datestr):
    is_time_re = re.compile('^[0-9]+:[0-9]+(:[0-9]+)?')
    is_date_re = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    d = t = None

    if is_time_re.match(datestr):
        t = time.fromisoformat(datestr)
    elif is_date_re.match(datestr):
        d = date.fromisoformat(datestr)
    else:
        try:
            dt = datetime.fromisoformat(datestr)
            d = dt.date()
            t = dt.time()
        except ValueError:
            raise RepcalConsoleException("Could not parse input '{}' as a date or time".format(datestr))

    return d, t


def get_default_date(args):
    if args.offset is not None:
        dt = datetime.now(timezone.utc)
        dt += timedelta(minutes=args.offset)
    elif args.paris_mean:
        dt = datetime.now(timezone.utc)
        dt += timedelta(minutes=9, seconds=21)
    else:
        dt = datetime.now()

    return dt.date(), dt.time()


def convert(d, t, output_format):
    default_format = []
    rdate = dtime = None

    if t is not None:
        dtime = DecimalTime.from_standard_time(t)
        default_format.append(DecimalTime.default_formatting)
    if d is not None:
        try:
            rdate = RepublicanDate.from_gregorian(d)
            default_format.append(RepublicanDate.default_formatting)
        except ValueError as e:
            raise RepcalConsoleException(e)

    default_format = ', '.join(default_format)
    formatter = RepublicanFormatter(rdate=rdate, dtime=dtime)

    try:
        date_string = formatter.format(output_format or default_format)
    except KeyError as e:
        raise RepcalConsoleException("Invalid format placeholder: {}".format(e))

    return date_string
