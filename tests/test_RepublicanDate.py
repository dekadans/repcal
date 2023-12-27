import unittest
from repcal import RepublicanDate
from datetime import date


class RepublicanDateTest(unittest.TestCase):
    def test_construct(self):
        d = RepublicanDate(200, 0, 0)
        self.assertEqual(200, d.year)
        self.assertEqual(0, d.month_index)
        self.assertEqual(0, d.month_day_index)

    def test_repr(self):
        d = RepublicanDate(200, 0, 0)
        self.assertEqual('repcal.RepublicanDate(200, 0, 0)', repr(d))

    def test_str(self):
        d = RepublicanDate(200, 0, 0)
        self.assertEqual('Primidi 1 vendémiaire an CC', str(d))

    def test_get_year(self):
        d1 = RepublicanDate(2, 0, 0)
        d2 = RepublicanDate(76, 0, 0)
        d3 = RepublicanDate(184, 0, 0)
        d4 = RepublicanDate(232, 0, 0)
        self.assertEqual(2, d1.get_year_arabic())
        self.assertEqual('II', d1.get_year_roman())
        self.assertEqual(76, d2.get_year_arabic())
        self.assertEqual('LXXVI', d2.get_year_roman())
        self.assertEqual(184, d3.get_year_arabic())
        self.assertEqual('CLXXXIV', d3.get_year_roman())
        self.assertEqual(232, d4.get_year_arabic())
        self.assertEqual('CCXXXII', d4.get_year_roman())

    def test_get_month(self):
        d1 = RepublicanDate(100, 0, 0)
        d2 = RepublicanDate(100, 4, 0)
        d3 = RepublicanDate(100, 8, 0)
        d4 = RepublicanDate(100, 11, 0)
        self.assertEqual(1, d1.get_month())
        self.assertEqual('Vendémiaire', d1.get_month_name())
        self.assertEqual(5, d2.get_month())
        self.assertEqual('Pluviôse', d2.get_month_name())
        self.assertEqual(9, d3.get_month())
        self.assertEqual('Prairial', d3.get_month_name())
        self.assertEqual(12, d4.get_month())
        self.assertEqual('Fructidor', d4.get_month_name())

    def test_get_week(self):
        d1 = RepublicanDate(100, 0, 0)
        d2 = RepublicanDate(100, 4, 24)
        self.assertEqual(1, d1.get_week())
        self.assertEqual(1, d1.get_week_in_year())
        self.assertEqual(3, d2.get_week())
        self.assertEqual(15, d2.get_week_in_year())

    def test_get_day(self):
        d1 = RepublicanDate(100, 0, 0)
        d2 = RepublicanDate(100, 8, 24)
        self.assertEqual(1, d1.get_day())
        self.assertEqual(1, d1.get_day_in_week())
        self.assertEqual(1, d1.get_day_in_year())
        self.assertEqual('Primidi', d1.get_day_name())
        self.assertEqual(25, d2.get_day())
        self.assertEqual(5, d2.get_day_in_week())
        self.assertEqual(265, d2.get_day_in_year())
        self.assertEqual('Quintidi', d2.get_day_name())

    def test_is_sansculottides(self):
        d1 = RepublicanDate(100, 0, 0)
        d2 = RepublicanDate(100, 12, 4)
        self.assertFalse(d1.is_sansculottides())
        self.assertTrue(d2.is_sansculottides())

    def test_is_leap_year(self):
        self.assertTrue(RepublicanDate.is_leap_year(3))
        self.assertTrue(RepublicanDate.is_leap_year(20))
        self.assertFalse(RepublicanDate.is_leap_year(33))
        self.assertFalse(RepublicanDate.is_leap_year(200))
        self.assertTrue(RepublicanDate.is_leap_year(204))
        self.assertFalse(RepublicanDate.is_leap_year(205))

    def test_from_gregorian_1(self):
        d1 = date.fromisoformat('1792-09-22')
        rd1 = RepublicanDate.from_gregorian(d1)
        self.assertEqual(1, rd1.get_year_arabic())
        self.assertEqual(1, rd1.get_day())
        self.assertEqual(1, rd1.get_month())

    def test_from_gregorian_2(self):
        d1 = date.fromisoformat('1792-09-21')
        with self.assertRaises(ValueError):
            RepublicanDate.from_gregorian(d1)

    def test_from_gregorian_3(self):
        d1 = date.fromisoformat('2002-06-12')
        rd1 = RepublicanDate.from_gregorian(d1)
        self.assertEqual(210, rd1.get_year_arabic())
        self.assertEqual(24, rd1.get_day())
        self.assertEqual(9, rd1.get_month())
        self.assertFalse(rd1.is_sansculottides())

    def test_from_gregorian_4(self):
        d1 = date.fromisoformat('2004-09-21')
        rd1 = RepublicanDate.from_gregorian(d1)
        self.assertEqual(212, rd1.get_year_arabic())
        self.assertEqual(6, rd1.get_day())
        self.assertEqual(13, rd1.get_month())
        self.assertTrue(rd1.is_sansculottides())

    def test_comparisons(self):
        d1 = date.fromisoformat('2023-01-14')
        d2 = date.fromisoformat('2023-07-30')
        d3 = date.fromisoformat('2023-12-31')
        rd1 = RepublicanDate.from_gregorian(d1)
        rd1_2 = RepublicanDate.from_gregorian(d1)
        rd2 = RepublicanDate.from_gregorian(d2)
        rd3 = RepublicanDate.from_gregorian(d3)

        self.assertTrue(rd1 == rd1_2)
        self.assertTrue(rd1 != rd2)
        self.assertFalse(rd1 != rd1)
        self.assertTrue(rd1 >= rd1_2)
        self.assertTrue(rd1 <= rd1_2)
        self.assertFalse(rd1 < rd1_2)
        self.assertFalse(rd1 > rd1_2)

        self.assertTrue(rd1 < rd2)
        self.assertTrue(rd2 > rd1)
        self.assertTrue(rd2 < rd3)
        self.assertTrue(rd3 > rd2)

        self.assertTrue(rd1 == d1)
        self.assertTrue(rd1 != d2)
        self.assertTrue(rd1 < d2)
        self.assertTrue(rd2 > d1)
