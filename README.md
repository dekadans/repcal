## Repcal

A python script that converts dates and time to the systems used by the French Republic from 1793 to 1805.

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


#### RepublicanDate instance methods

| Method              | Example return value |
| ------------------- | -------------------- |
| get_year_arabic()   | _219_                |
| get_year_roman()    | _CCXXIX_             |
| get_month()         | _Vendémiaire_        |
| get_week_number()   | _3_                  |
| get_day()           | _28_                 |
| get_weekday()       | _octidi_             |
| is_sansculottides() | _false_              |

Note that for compatibility purposes, if the date is a complementary day then _get_month()_
will return "Sansculottides" despite this not being an actual month.

### As a script

```
$ python3 -m repcal
8:1:65, octidi 28 Vendémiaire an CCXXIX
```


### Todo
* Rural calendar items
* More cli functionality