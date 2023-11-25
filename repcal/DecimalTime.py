from datetime import datetime, date, time
from math import floor
from typing import Self
from .RepublicanFormatter import RepublicanFormatter


class DecimalTime:
    default_formatting = '{%H}:{%M}:{%S}'

    def __init__(self, hour: int, minute: int, second: int):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.decimal = self._make_decimal_value()

    def __str__(self) -> str:
        return self.get_formatter().format(self.default_formatting)

    def get_formatter(self) -> RepublicanFormatter:
        return RepublicanFormatter(dtime=self)

    def _make_decimal_value(self) -> str:
        if max(self.hour, self.minute, self.second) == 0:
            return '0'

        h = self.hour
        m = f'{self.minute:02}' if max(self.minute, self.second) > 0 else ''
        s = f'{self.second:02}' if self.second > 0 else ''
        return f'0,{h}{m}{s}'.rstrip('0')

    @classmethod
    def from_standard_time(cls, standard_time: time) -> Self:
        """
        Takes a time object and converts to decimal.
        """
        midnight = datetime.combine(date.today(), time.fromisoformat('00:00:00'))
        target = datetime.combine(date.today(), standard_time)

        # Correct for timezone-aware input
        if target.tzinfo is not None and target.tzinfo.utcoffset(target) is not None:
            midnight = midnight.astimezone(target.tzinfo)

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
