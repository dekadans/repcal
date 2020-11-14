## Repcal

A script that converts date and time to the systems used by the French Republic, the calendar from 1793 to 1805 and decimal time for about a year between 1794 and 1795.
More information can be found on [Wikipedia](https://en.wikipedia.org/wiki/French_Republican_calendar).

It uses the Romme method of calculating leap years, as in keeping the ones used by the French Republic and using the Gregorian rules for the years after the calendar was abolished.

### Installation

```
$ pip install repcal
```

### Usage

The current local time is used by default.

```
$ repcal
5:80:63, quartidi 24 Brumaire an CCXXIX
```

Or, for the full Republican experience, it can default to Paris Mean Time (6.49 decimal minutes ahead of GMT).

```
$ repcal --paris-mean
5:45:47, quartidi 24 Brumaire an CCXXIX
```

It also accepts date, time and format as arguments.

```
$ repcal '1969-07-20 20:17:40'
8:45:60, primidi 1 Thermidor an CLXXVII

$ repcal '1969-07-20'
primidi 1 Thermidor an CLXXVII

$ repcal '20:17:40'
8:45:60

$ repcal '1969-07-20' --format '{%d} {%B}'
1 Thermidor
```

### As a Python package

```python
from repcal import RepublicanDate, DecimalTime
from datetime import datetime

n = datetime.now()
rd = RepublicanDate.from_gregorian(n.date())
dt = DecimalTime.from_standard_time(n.time())

print(rd) # quartidi 24 Brumaire an CCXXIX
print(dt) # 5:79:47
```

### RepublicanDate API

| Value            | Instance method     | Format placeholder | Example               |
| ---------------- | ------------------- | ------------------ | --------------------- |
| Year (arabic)    | get_year_arabic()   | %y                 | _219_                 |
| Year (roman)     | get_year_roman()    | %Y                 | _CCXXIX_              |
| Month            | get_month()         | %B                 | _Vendémiaire_         |
| Week (décade)    | get_week_number()   | %W                 | _3_                   |
| Day in month     | get_day()           | %d                 | _28_                  |
| Day in week      | get_weekday()       | %A                 | _octidi_              |
| Is complementary | is_sansculottides() | --                 | _false_               |


### DecimalTime API

| Value            | Property | Format placeholder | Example               |
| ---------------- | -------- | ------------------ | --------------------- |
| Hour             | hour     | %H                 | _8_                   |
| Minute           | minute   | %M                 | _1_                   |
| Second           | second   | %S                 | _65_                  |

