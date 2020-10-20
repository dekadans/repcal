class RepublicanFormatter:
    def __init__(self, rdate=None, dtime=None):
        """
        :param rdate: RepublicanDate
        :param dtime: DecimalTime
        """
        self.rdate = rdate
        self.dtime = dtime

    def format(self, fstring: str):
        fstring = self._clean(fstring)
        return fstring.format(**self._data())

    def _clean(self, fstring: str):
        if self.rdate is not None and self.rdate.is_sansculottides():
            fstring = fstring.replace('{%d}', '').replace('{%B}', '')
            fstring = ' '.join(fstring.split())

        return fstring

    def _data(self):
        time_data = date_data = {}

        if self.rdate is not None:
            date_data = {
                '%Y': self.rdate.get_year_roman(),
                '%y': self.rdate.get_year_arabic(),
                '%B': self.rdate.get_month(),
                '%W': self.rdate.get_week_number(),
                '%d': self.rdate.get_day(),
                '%A': self.rdate.get_weekday()
            }

        if self.dtime is not None:
            time_data = {
                '%H': self.dtime.hour,
                '%M': self.dtime.minute,
                '%S': self.dtime.second
            }

        return {**time_data, **date_data}
