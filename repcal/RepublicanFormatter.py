import os


class RepublicanFormatter:
    """
    Utility for creating republican date/time strings using format placeholders.
    """

    time_default = '{%H}:{%M}:{%S}'
    date_default = '{%+A} {%d} {%B} an {%Y}'

    def __init__(self, rdate=None, dtime=None):
        """
        :type rdate: repcal.RepublicanDate.RepublicanDate | None
        :type dtime: repcal.DecimalTime.DecimalTime | None
        """
        self.date = rdate
        self.time = dtime

    def format(self, fstring: str | None) -> str:
        """
        Format the date and/or time using a string with placeholders for temporal properties.
        If given None it will use default patterns.
        """
        return (fstring or self.default()).format(**self._data())

    def default(self) -> str:
        tf = os.environ.get('REPCAL_TIME_FORMAT') or self.time_default
        df = os.environ.get('REPCAL_DATE_FORMAT') or self.date_default

        default_format = []
        if self.time is not None:
            default_format.append(tf)
        if self.date is not None:
            default_format.append(df)

        return ' - '.join(default_format)

    def _data(self) -> dict:
        time_data = date_data = {}

        if self.date is not None:
            date_data = {
                '%Y': self.date.get_year_roman(),
                '%y': self.date.get_year_arabic(),
                '%m': self.date.get_month(),
                '%B': self.date.get_month_name().lower(),
                '%+B': self.date.get_month_name(),
                '%W': self.date.get_week(),
                '%U': self.date.get_week_in_year(),
                '%d': self.date.get_day(),
                '%w': self.date.get_day_in_week(),
                '%j': self.date.get_day_in_year(),
                '%A': self.date.get_day_name().lower(),
                '%+A': self.date.get_day_name()
            }

        if self.time is not None:
            time_data = {
                '%H': self.time.hour,
                '%M': self.time.minute,
                '%S': self.time.second,
                '%D': self.time.decimal
            }

        return {**time_data, **date_data}
