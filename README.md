# Repcal

A small application that converts date and time to the systems used by the French First Republic.

The calendar from 1793 to 1805 and decimal time for about a year between 1794 and 1795. More information can be found on [Wikipedia](https://en.wikipedia.org/wiki/French_Republican_calendar).

It uses the Romme method of calculating leap years, as in keeping the ones used by the French Republic and using the Gregorian rules for the years after the calendar was abolished.

## CLI Tool

Installation using [pipx](https://github.com/pypa/pipx):

```
$ pipx install repcal
```

When called without any parameters it will print the current local time and date:

```
$ repcal
7:76:5 - Septidi 7 nivôse an CCXXXII
```

### Conversions

`-i DATE, --input DATE`

This parameter accepts a specific date and/or time in ISO format and will print it's republican counterpart.

```
$ repcal -i '1969-07-20 20:17:40'
8:45:60 - Primidi 1 thermidor an CLXXVII
```

### UTC Offset

`-u OFFSET, --utc-offset OFFSET`

This parameter is used to get the current date and time for a given number of standard minutes from UTC. For example, the current time in New York (EST, UTC-05:00):

```
$ repcal -u -300
```

### Paris Mean Time

`-p, --paris-mean`

For the full republican experience, it can also use Paris Mean Time (6.49 decimal minutes ahead of UTC).

### Output Formatting

`-f [FORMAT], --format [FORMAT]`

The default output format can be overridden with a string containing placeholders for specific datetime values.

```
$ repcal -i '1969-07-20' -f '{%d} {%+B}'
1 Thermidor
```

Using `-f, --format` without a provided format string will print a [cheat sheet](repcal/format_hints.py) of available placeholders.

The format can also be set using the environment variables `REPCAL_DATE_FORMAT` and `REPCAL_TIME_FORMAT`:

```
$ REPCAL_DATE_FORMAT='{%d} {%+B}' repcal -i '1969-07-20'
```


## Python Package

The script can also installed with `pip` and used as a package in other Python projects:

```python  
from repcal import RepublicanDate, DecimalTime
from datetime import datetime

n = datetime.fromisoformat('1969-07-20 20:17:40')
rd = RepublicanDate.from_gregorian(n.date())
dt = DecimalTime.from_standard_time(n.time())

# The objects have standard string representations,...
print(rd) # Primidi 1 thermidor an CLXXVII
print(dt) # 8:45:60

# ...access to specific properties...
print(rd.get_year_roman()) # CLXXVII
print(dt.decimal) # 0,8456

# ...and formatting.
print(rd.get_formatter().format('{%d} {%+B}')) # 1 Thermidor
```