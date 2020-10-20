from datetime import datetime
from .RepublicanDate import RepublicanDate
from .DecimalTime import DecimalTime


t = datetime.utcnow()

dtime = DecimalTime.from_standard_time(t.time())
rdate = RepublicanDate.from_gregorian(t.date())

print('{}, {}'.format(
    dtime,
    rdate
))
