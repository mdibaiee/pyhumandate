import unittest
import datetime
from datetime import timedelta
from index import parse_date, days, months, years, tokenize

class HumanDateTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.today = datetime.date.today()

    def test_weekdays(self):
        for (i, d) in enumerate(days):
            self.assertEqual(parse_date(d).weekday(), i % 7)

        for (i, d) in enumerate(days):
            self.assertEqual(parse_date('past {}'.format(d)).weekday(), i % 7)

    def test_months(self):
        for (i, m) in enumerate(months):
            self.assertEqual(parse_date(m).month, i % 12 + 1)

        for (i, m) in enumerate(months):
            self.assertEqual(parse_date('past {}'.format(m)).month, i % 12 + 1)

    def test_years(self):
        for y in years:
            self.assertEqual(parse_date(y).year, int(y))

    def test_time(self):
        tests = {
            '00:00': (0, 0),
            '0:0'  : (0, 0),
            '12:00': (12, 0),
            '12:0' : (12, 0),
            '24:00': (self.now.hour, self.now.minute),
            '10:60': (self.now.hour, self.now.minute),
            '23:59': (23, 59),
            'at 12': (12, 0),
            'at 24': (self.now.hour, self.now.minute),
            '12AM' : (0, 0),
            '12PM' : (12, 0),
            '11PM' : (23, 0),
            '12 AM': (0, 0),
            '5 pm' : (17, 0),
        }

        for (k, (h, m)) in tests.items():
            d = parse_date(k)
            self.assertEqual((d.hour, d.minute), (h, m))

    def test_day_of_month(self):
        tests = {
            '12 jan': (12, 1),
            '28 february': (28, 2),
            '1th december': (1, 12),
            'jan 12': (12, 1),
            'february 28': (28, 2),
            'december 1th': (1, 12),
            'Feb. 28': (28, 2),
        }

        for (k, (day, m)) in tests.items():
            d = parse_date(k)
            self.assertEqual((d.day, d.month), (day, m))

    def test_relative_future_dates(self):
        tests = {
            'next week': self.today + timedelta(days=7),
            'next 2 weeks': self.today + timedelta(days=7*2),
            'in 2 weeks': self.today + timedelta(days=7*2),
            'next fortnight': self.today + timedelta(days=7*2),
            'next month': self.today + timedelta(days=30),
            'next year': self.today + timedelta(days=365),
            'this week': self.today,
            'this month': self.today,
            'this year': self.today,
            'tomorrow!': self.today + timedelta(days=1),
        }

        for (k, date) in tests.items():
            d = parse_date(k)
            self.assertEqual(d.date(), date)

    def test_relative_future_times(self):
        tests = {
            '2 seconds': (self.now.hour, self.now.minute, self.now.second + 2),
            '3 minute': (self.now.hour, self.now.minute + 3, self.now.second),
            '10 hours': ((self.now.hour + 10) % 24, self.now.minute, self.now.second),
        }

        for (k, t) in tests.items():
            d = parse_date(k)
            self.assertEqual((d.hour, d.minute, d.second), t)

    def test_relative_past_dates(self):
        tests = {
            'past week': self.today - timedelta(days=7),
            'past 2 weeks': self.today - timedelta(days=7*2),
            'last 2 weeks': self.today - timedelta(days=7*2),
            'past fortnight': self.today - timedelta(days=7*2),
            'past month': self.today - timedelta(days=30),
            'past year': self.today - timedelta(days=365),
            'a week ago': self.today - timedelta(days=7),
            'a month ago': self.today - timedelta(days=30),
            'a year past': self.today - timedelta(days=365),
            'yesterday': self.today - timedelta(days=1),
        }

        for (k, date) in tests.items():
            d = parse_date(k)
            self.assertEqual(d.date(), date)

    def test_relative_past_times(self):
        tests = {
            '2 seconds ago': (self.now.hour, self.now.minute, self.now.second - 2),
            'past 3 minute': (self.now.hour, self.now.minute - 3, self.now.second),
            'last 10 hours': ((self.now.hour - 10) % 24, self.now.minute, self.now.second),
            'an hour ago': ((self.now.hour - 1), self.now.minute, self.now.second),
        }

        for (k, t) in tests.items():
            d = parse_date(k)
            self.assertEqual((d.hour, d.minute, d.second), t)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
