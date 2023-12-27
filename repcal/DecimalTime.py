from datetime import datetime, date, time
from math import floor
from typing import Self
from .RepublicanFormatter import RepublicanFormatter
import operator


class DecimalTime:
    """
    A point in time in a 10-hour representation.
    Format codes:
    Hour: %H
    Minute: %M
    Second: %S
    Decimal value: %D
    """

    def __init__(self, hour: int, minute: int, second: int):
        self.hour: int = hour
        self.minute: int = minute
        self.second: int = second
        self.decimal: str = self._make_decimal_value()

    def __str__(self) -> str:
        return self.get_formatter().format(None)

    def get_formatter(self) -> RepublicanFormatter:
        return RepublicanFormatter(dtime=self)

    def _make_decimal_value(self) -> str:
        if max(self.hour, self.minute, self.second) == 0:
            return '0'

        h = self.hour
        m = f'{self.minute:02}' if max(self.minute, self.second) > 0 else ''
        s = f'{self.second:02}' if self.second > 0 else ''
        return f'0,{h}{m}{s}'.rstrip('0')

    def __repr__(self) -> str:
        return 'repcal.DecimalTime({}, {}, {})'.format(
            self.hour,
            self.minute,
            self.second
        )

    def _compare(self, other, op):
        if isinstance(other, time):
            other = DecimalTime.from_standard_time(other)

        if isinstance(other, DecimalTime):
            one = (self.hour, self.minute, self.second)
            two = (other.hour, other.minute, other.second)
            return op(one, two)

        return NotImplemented

    def __eq__(self, other):
        return self._compare(other, operator.eq)

    def __lt__(self, other):
        return self._compare(other, operator.lt)

    def __le__(self, other):
        return self._compare(other, operator.le)

    def __gt__(self, other):
        return self._compare(other, operator.gt)

    def __ge__(self, other):
        return self._compare(other, operator.ge)

    @classmethod
    def from_standard_time(cls, standard_time: time) -> Self:
        """
        Converts regular 24-hour time to 10-hour decimal time.
        Creates a DecimalTime object from a datetime.time.
        """

        # Correct for timezone-aware input
        if standard_time.tzinfo is not None:
            standard_time = standard_time.replace(tzinfo=None)

        midnight = datetime.combine(date.today(), time.fromisoformat('00:00:00'))
        target = datetime.combine(date.today(), standard_time)

        standard_seconds = (target - midnight).seconds

        second_ratio = (100 * 100 * 10) / (60 * 60 * 24)
        decimal_seconds = floor(standard_seconds * second_ratio)

        seconds_per_hour = 100 * 100
        seconds_per_minute = 100

        hour = decimal_seconds // seconds_per_hour
        decimal_seconds -= hour * seconds_per_hour

        minute = decimal_seconds // seconds_per_minute
        decimal_seconds -= minute * seconds_per_minute

        return cls(hour, minute, decimal_seconds)
