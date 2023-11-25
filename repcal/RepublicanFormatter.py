class RepublicanFormatter:
    """
    Utility for creating republican date/time strings using format placeholders.
    """

    def __init__(self, rdate=None, dtime=None):
        """
        :type rdate: repcal.RepublicanDate.RepublicanDate | None
        :type dtime: repcal.DecimalTime.DecimalTime | None
        """
        self.date = rdate
        self.time = dtime

    def format(self, fstring: str) -> str:
        return fstring.format(**self._data())

    def _data(self) -> dict:
        time_data = date_data = {}

        if self.date is not None:
            date_data = {
                '%Y': self.date.get_year_roman(),
                '%y': self.date.get_year_arabic(),
                '%m': self.date.get_month(),
                '%B': self.date.get_month_name().lower(),
                '%W': self.date.get_week(),
                '%U': self.date.get_week_in_year(),
                '%d': self.date.get_day(),
                '%w': self.date.get_day_in_week(),
                '%j': self.date.get_day_in_year(),
                '%A': self.date.get_day_name().lower()
            }

        if self.time is not None:
            time_data = {
                '%H': self.time.hour,
                '%M': self.time.minute,
                '%S': self.time.second,
                '%D': self.time.decimal
            }

        return {**time_data, **date_data}
