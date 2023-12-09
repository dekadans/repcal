import unittest
from repcal import DecimalTime
from datetime import time


class DecimalTimeTest(unittest.TestCase):
    def test_construct(self):
        d = DecimalTime(0, 0, 0)
        self.assertEqual(0, d.hour)
        self.assertEqual(0, d.minute)
        self.assertEqual(0, d.second)

    def test_from_standard_at_midnight(self):
        t = time.fromisoformat('00:00:00')
        d = DecimalTime.from_standard_time(t)
        self.assertEqual(0, d.hour)
        self.assertEqual(0, d.minute)
        self.assertEqual(0, d.second)
        self.assertEqual('0', d.decimal)

    def test_from_standard_in_morning(self):
        t = time.fromisoformat('07:43:19')
        d = DecimalTime.from_standard_time(t)
        self.assertEqual(3, d.hour)
        self.assertEqual(21, d.minute)
        self.assertEqual(74, d.second)
        self.assertEqual('0,32174', d.decimal)

    def test_timezone_aware(self):
        t = time.fromisoformat('07:43:19T+0200')
        d = DecimalTime.from_standard_time(t)
        self.assertEqual(3, d.hour)
        self.assertEqual(21, d.minute)
        self.assertEqual(74, d.second)

    def test_decimal_no_trailing_zeroes(self):
        d = DecimalTime(1, 0, 0)
        self.assertEqual('0,1', d.decimal)

    def test_decimal_one_second(self):
        d = DecimalTime(0, 0, 1)
        self.assertEqual('0,00001', d.decimal)

    def test_str(self):
        d = DecimalTime(3, 21, 74)
        self.assertEqual('3:21:74', str(d))

    def test_repr(self):
        d = DecimalTime(3, 21, 74)
        self.assertEqual('repcal.DecimalTime(3, 21, 74)', repr(d))

