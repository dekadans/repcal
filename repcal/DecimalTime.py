from datetime import datetime, date, time
from math import floor
from .RepublicanFormatter import RepublicanFormatter


class DecimalTime:
    default_formatting = '{%H}:{%M}:{%S}'

    def __init__(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return self.get_formatter().format(self.default_formatting)

    def get_formatter(self):
        return RepublicanFormatter(dtime=self)

    @classmethod
    def from_standard_time(cls, standard_time):
        """
        Takes a time object and converts to decimal.
        If adjust_to_paris_mean is true the given time will be assumed to be GMT
        and the resulting decimal time is adjusted to Paris Mean Time.
        Note: if we're adjusting to Paris time, moments close to midnight GMT
        will result in a date turnover

        :param standard_time: datetime.time
        :return: string
        """
        midnight = datetime.combine(date.today(), time.fromisoformat('00:00:00'))
        target = datetime.combine(date.today(), standard_time)

        standard_seconds = (target - midnight).seconds

        second_ratio = 100 * 100 * 10 / (60 * 60 * 24)
        decimal_seconds = floor(standard_seconds * second_ratio)

        seconds_per_hour = 100 * 100
        seconds_per_minute = 100

        hour = decimal_seconds // seconds_per_hour
        decimal_seconds -= hour * seconds_per_hour

        minute = decimal_seconds // seconds_per_minute
        decimal_seconds -= minute * seconds_per_minute

        return cls(hour, minute, decimal_seconds)
