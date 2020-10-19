## Repcal

### As a package

```python
from repcal import RepublicanDate, DecimalTime
from datetime import datetime

n = datetime.utcnow()
rd = RepublicanDate.from_gregorian(n.date())
dt = DecimalTime.from_standard_time(n.time())

print(str(rd)) # octidi 28 Vendémiaire an CCXXIX
print(str(dt)) # 8:1:65
```

### As a script

```
$ python3 -m repcal
8:1:65, octidi 28 Vendémiaire an CCXXIX
```