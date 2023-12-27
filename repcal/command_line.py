import argparse
from .RepublicanDate import RepublicanDate
from .DecimalTime import DecimalTime
from .RepublicanFormatter import RepublicanFormatter
from datetime import datetime, timedelta, time, date, timezone
import re
import logging
from .format_hints import format_intro, date_table, time_table


class RepcalConsoleException(Exception):
    pass


class WrappedDateTime:
    def __init__(self, d: date | None, t: time | None):
        self.date = d
        self.time = t


def main():
    logging.basicConfig(format='%(levelname)s: %(message)s')
    read_more = 'Read more about usage at: https://github.com/dekadans/repcal'
    parser = argparse.ArgumentParser(prog='repcal', description='Converts and prints date and time in the French Republican style.', epilog=read_more)

    parser.add_argument('-i', '--input', help='ISO formatted date and/or time to convert.', metavar='DATE')
    parser.add_argument('-u', '--utc-offset', help='Convert the current time with the given offset in minutes from UTC.', metavar='OFFSET', type=int)
    parser.add_argument('-p', '--paris-mean', action='store_true', help='Use Paris Mean Time as offset (6.49 decimal minutes ahead of UTC).')

    parser.add_argument('-f', '--format', help='Explicitly set the output format. An empty argument will print available formatting.', nargs='?', default='default')

    args = parser.parse_args()

    try:
        validate_args(args)
        if args.input is not None:
            dt = parse_date(args.input)
        else:
            dt = get_default_date(args)

        formatter = create_formatter(dt)
        output_format = get_format(args.format, formatter)
        try:
            result = formatter.format(output_format)
        except KeyError as e:
            raise RepcalConsoleException("Invalid format placeholder: {}".format(e))
    except RepcalConsoleException as e:
        logging.error(e)
        exit(1)

    print(result)


def validate_args(args):
    has_input = args.input is not None
    has_offset = args.utc_offset is not None
    has_paris = args.paris_mean is True

    active = [m for m in [has_input, has_offset, has_paris] if m is True]

    if len(active) > 1:
        raise RepcalConsoleException("The different input arguments (-i, -u, -p) are mutually exclusive.")

    if args.utc_offset is not None and not (-1440 < args.utc_offset < 1440):
        raise RepcalConsoleException('The offset must be within 24 hours from UTC.')


def parse_date(datestr: str) -> WrappedDateTime:
    is_time_re = re.compile('^[0-9]{2}:[0-9]{2}(:[0-9]{2})?$')
    is_date_re = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    d = t = None

    try:
        if is_time_re.match(datestr):
            t = time.fromisoformat(datestr)
        elif is_date_re.match(datestr):
            d = date.fromisoformat(datestr)
        else:
            dt = datetime.fromisoformat(datestr)
            d = dt.date()
            t = dt.time()
    except ValueError:
        raise RepcalConsoleException("Could not parse input '{}' as a date or time".format(datestr))

    return WrappedDateTime(d, t)


def get_default_date(args) -> WrappedDateTime:
    if args.utc_offset is not None:
        dt = datetime.now(timezone.utc)
        dt += timedelta(minutes=args.utc_offset)
    elif args.paris_mean:
        dt = datetime.now(timezone.utc)
        dt += timedelta(minutes=9, seconds=21)
    else:
        dt = datetime.now()

    return WrappedDateTime(dt.date(), dt.time())


def create_formatter(wrapped: WrappedDateTime) -> RepublicanFormatter:
    rdate = dtime = None

    if wrapped.time is not None:
        dtime = DecimalTime.from_standard_time(wrapped.time)
    if wrapped.date is not None:
        try:
            rdate = RepublicanDate.from_gregorian(wrapped.date)
        except ValueError as e:
            raise RepcalConsoleException(e)

    return RepublicanFormatter(rdate=rdate, dtime=dtime)


def get_format(format_arg: str | None, dt: RepublicanFormatter) -> str:
    default_format = dt.default()

    if format_arg is None:
        default = re.sub('([{}])', r'\1'*2, default_format)
        helptext = format_intro.format(default)

        if dt.date is not None:
            helptext += date_table
        if dt.time is not None:
            helptext += time_table

        return helptext

    if format_arg != 'default':
        return format_arg

    return default_format
