from datetime import date
from .RepublicanFormatter import RepublicanFormatter


class RepublicanDate:
    default_formatting = '{%A} {%d} {%B} an {%Y}'

    months = ('Vendémiaire', 'Brumaire', 'Frimaire', 'Nivôse', 'Pluviôse', 'Ventôse',
              'Germinal', 'Floréal', 'Prairial', 'Messidor', 'Thermidor', 'Fructidor',
              'Sansculottides')

    days = ('primidi', 'duodi', 'tridi', 'quartidi', 'quintidi',
            'sextidi', 'septidi', 'octidi', 'nonidi', 'décadi')

    sansculottides = (
        'La Fête de la Vertu',
        'La Fête du Génie',
        'La Fête du Travail',
        'La Fête de l\'Opinion',
        'La Fête des Récompenses',
        'La Fête de la Révolution'
    )

    def __init__(self, year, month_index, month_day_index, week_day_index):
        self.year = year
        self.month_index = month_index
        self.month_day_index = month_day_index
        self.week_day_index = week_day_index

    def __str__(self):
        return self.get_formatter().format(self.default_formatting)

    def get_formatter(self):
        return RepublicanFormatter(rdate=self)

    def get_year_arabic(self):
        return self.year

    def get_year_roman(self):
        letters = (
            ('C', 100),
            ('XC', 90),
            ('L', 50),
            ('XL', 40),
            ('X', 10),
            ('IX', 9),
            ('V', 5),
            ('IV', 4),
            ('I', 1)
        )

        roman = ''
        years_left = self.year

        for combination in letters:
            while years_left >= combination[1]:
                roman += combination[0]
                years_left -= combination[1]

        return roman

    def get_month(self):
        return self.months[self.month_index]

    def get_week_number(self):
        return str(self.month_day_index // 10 + 1)

    def get_day(self):
        return str(self.month_day_index+1)

    def get_weekday(self):
        if self.is_sansculottides():
            return self.sansculottides[self.week_day_index]
        else:
            return self.days[self.week_day_index]

    def is_sansculottides(self):
        return self.month_index == 12

    @classmethod
    def from_gregorian(cls, date_to_convert):
        """
        Converts a gregorian date to the corresponding date in the French republican calendar
        :param date_to_convert: datetime.date
        :return: RepublicanDate
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
        day_in_week = day_in_month % 10

        return cls(year, month, day_in_month, day_in_week)

    @staticmethod
    def is_leap_year(year):
        """
        Determines if a year in the French Republican calendar is a leap year
        :param year: int
        :return: Boolean
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
