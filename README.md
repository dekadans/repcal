## Repcal

A python script that converts dates and time to the systems used by the French Republic from 1793 to 1805.

It uses the Romme method of calculating leap years, as in keeping the ones used by the French Republic and using the Gregorian rules for the years after the calendar was abolished.

### As a package

```python
from repcal import RepublicanDate, DecimalTime
from datetime import datetime

n = datetime.utcnow()
rd = RepublicanDate.from_gregorian(n.date())
dt = DecimalTime.from_standard_time(n.time())

print(rd) # octidi 28 Vendémiaire an CCXXIX
print(dt) # 8:1:65
```

### As a script

_The script uses Paris Mean Time (6.49 decimal minutes ahead of GMT)._

```
$ python3 -m repcal
8:1:65, octidi 28 Vendémiaire an CCXXIX

$ python3 -m repcal '1969-07-20' --format '{%d} {%B}'
1 Thermidor
```


### API and formatting options

| Value            | Instance method/property | Format placeholder | Example               |
| ---------------- | ------------------------ | ------------------ | --------------------- |
| Year (arabic)    | get_year_arabic()        | %y                 | _219_                 |
| Year (roman)     | get_year_roman()         | %Y                 | _CCXXIX_              |
| Month            | get_month()              | %B                 | _Vendémiaire_         |
| Week (décade)    | get_week_number()        | %W                 | _3_                   |
| Day in month     | get_day()                | %d                 | _28_                  |
| Day in week      | get_weekday()            | %A                 | _octidi_              |
| Is complementary | is_sansculottides()      | --                 | _false_               |
| Hour             | hour                     | %H                 | _8_                   |
| Minute           | minute                   | %M                 | _1_                   |
| Second           | second                   | %S                 | _65_                  |

