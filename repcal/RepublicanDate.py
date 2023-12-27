from datetime import date
from typing import Self
from .RepublicanFormatter import RepublicanFormatter
import operator


class RepublicanDate:
    """
    A date in the French Republican calendar.
    """

    months = ['Vendémiaire', 'Brumaire', 'Frimaire', 'Nivôse', 'Pluviôse', 'Ventôse',
              'Germinal', 'Floréal', 'Prairial', 'Messidor', 'Thermidor', 'Fructidor',
              'Jour complémentaire']

    days = ['Primidi', 'Duodi', 'Tridi', 'Quartidi', 'Quintidi',
            'Sextidi', 'Septidi', 'Octidi', 'Nonidi', 'Décadi']

    def __init__(self, year: int, month_index: int, month_day_index: int):
        self.year = year
        self.month_index = month_index
        self.month_day_index = month_day_index
        self.week_day_index = month_day_index % 10

    def __str__(self) -> str:
        return self.get_formatter().format(None)

    def get_formatter(self) -> RepublicanFormatter:
        return RepublicanFormatter(rdate=self)

    def get_year_arabic(self) -> int:
        """
        Get the year as integer.
        Example: 232
        Format code: %y
        """
        return self.year

    def get_year_roman(self) -> str:
        """
        Get the year as roman numeral.
        Example: CCXXXII
        Format code: %Y
        """
        letters = [
            ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400),
            ('C', 100), ('XC', 90), ('L', 50), ('XL', 40),
            ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1)
        ]

        roman = ''
        years_left = self.year

        for letter, value in letters:
            while years_left >= value:
                roman += letter
                years_left -= value

        return roman

    def get_month(self) -> int:
        """
        Get the numeric representation of the month.
        Regular months 1-12, complementary days will return 13.
        Format code: %m
        """
        return self.month_index + 1

    def get_month_name(self) -> str:
        """
        Get the textual representation of the month.
        Example: Vendémiaire
        Format code: %B
        """
        return self.months[self.month_index]

    def get_week(self) -> int:
        """
        The _décade_. The numeric representation of the week within the current month (1-3).
        Format code: %W
        """
        return self.month_day_index // 10 + 1

    def get_week_in_year(self) -> int:
        """
        The numeric representation of the week within the year (1-37).
        Format code: %U
        """
        return (self.month_index * 3) + self.get_week()

    def get_day(self) -> int:
        """
        The numeric representation of the day within the current month (1-30).
        Format code: %d
        """
        return self.month_day_index + 1

    def get_day_in_week(self) -> int:
        """
        The numeric representation of the day within the current week (1-10).
        Format code: %w
        """
        return self.week_day_index + 1

    def get_day_in_year(self) -> int:
        """
        The numeric representation of the day within the current year (1-365/366).
        Format code: %j
        """
        return (self.month_index * 30) + self.month_day_index + 1

    def get_day_name(self) -> str:
        """
        Get the textual representation of the day.
        Example: Primidi
        Format code: %A
        """
        return self.days[self.week_day_index]

    def is_sansculottides(self) -> bool:
        """
        Check if the day is complementary (True/False).
        """
        return self.month_index == 12

    def __repr__(self) -> str:
        return 'repcal.RepublicanDate({}, {}, {})'.format(
            self.year,
            self.month_index,
            self.month_day_index
        )

    def _compare(self, other, op):
        if isinstance(other, date):
            other = RepublicanDate.from_gregorian(other)

        if isinstance(other, RepublicanDate):
            one = (self.year, self.month_index, self.month_day_index)
            two = (other.year, other.month_index, other.month_day_index)
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
    def from_gregorian(cls, date_to_convert: date) -> Self:
        """
        Converts a gregorian date to the corresponding date in the French republican calendar.
        Creates a RepublicanDate object from a datetime.date.
        """
        start = date(1792, 9, 22)

        if date_to_convert < start:
            raise ValueError('Provided date is before the adoption of the calendar')

        delta = date_to_convert - start
        day_diff = delta.days + 1  # Inclusive

        year = 1
        start_day = 1

        while True:
            end_day = start_day + (365 if cls.is_leap_year(year) else 364)

            if end_day >= day_diff:
                break

            year += 1
            start_day = end_day + 1

        day_in_year = day_diff - start_day

        month = day_in_year // 30
        day_in_month = day_in_year % 30

        return cls(year, month, day_in_month)

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        Determines if a year in the French Republican calendar is a leap year.
        """
        if year < 1:
            raise ValueError('Year is less than one')

        first_leap_years = [3, 7, 11, 15, 20]
        if year <= max(first_leap_years):
            return year in first_leap_years

        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                else:
                    return False

            return True

        return False
