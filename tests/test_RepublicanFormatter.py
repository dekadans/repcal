import unittest
from datetime import date, time
from repcal import RepublicanDate, RepublicanFormatter, DecimalTime


class RepublicanFormatterTest(unittest.TestCase):
    def test_date_placeholders(self):
        d = date.fromisoformat('2023-06-17')
        rd = RepublicanDate.from_gregorian(d)
        f = RepublicanFormatter(rdate=rd)

        self.assertEqual(f.format('{%Y}'), rd.get_year_roman())
        self.assertEqual(f.format('{%y}'), str(rd.get_year_arabic()))
        self.assertEqual(f.format('{%m}'), str(rd.get_month()))
        self.assertEqual(f.format('{%B}'), rd.get_month_name().lower())
        self.assertEqual(f.format('{%+B}'), rd.get_month_name())
        self.assertEqual(f.format('{%W}'), str(rd.get_week()))
        self.assertEqual(f.format('{%U}'), str(rd.get_week_in_year()))
        self.assertEqual(f.format('{%d}'), str(rd.get_day()))
        self.assertEqual(f.format('{%w}'), str(rd.get_day_in_week()))
        self.assertEqual(f.format('{%j}'), str(rd.get_day_in_year()))
        self.assertEqual(f.format('{%A}'), rd.get_day_name().lower())
        self.assertEqual(f.format('{%+A}'), rd.get_day_name())

    def test_time_placeholders(self):
        t = time.fromisoformat('20:47:18')
        dt = DecimalTime.from_standard_time(t)
        f = RepublicanFormatter(dtime=dt)

        self.assertEqual(f.format('{%H}'), str(dt.hour))
        self.assertEqual(f.format('{%M}'), str(dt.minute))
        self.assertEqual(f.format('{%S}'), str(dt.second))
        self.assertEqual(f.format('{%D}'), dt.decimal)

    def test_invalid_placeholder(self):
        t = time.fromisoformat('20:47:18')
        dt = DecimalTime.from_standard_time(t)
        f = RepublicanFormatter(dtime=dt)

        with self.assertRaises(KeyError):
            f.format('{what}')
