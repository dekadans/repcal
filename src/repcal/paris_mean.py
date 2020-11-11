from datetime import timedelta
from .RepublicanDate import RepublicanDate
from .DecimalTime import DecimalTime


def paris_mean(datetime):
    """
    A GMT datetime is converted to Republican Paris Mean Time
    :param datetime: datetime
    :return: RepublicanDate, DecimalTime
    """
    dtime = DecimalTime.from_standard_time(datetime.time(), adjust_to_paris_mean=True)

    if dtime.date_turnover:
        datetime += timedelta(days=1)

    rdate = RepublicanDate.from_gregorian(datetime.date())

    return rdate, dtime
