import re
import time
import calendar

def parse_time(times_str):
    matches = re.match(
        r'/Date\((\d{10})\d+[+-]\d+\)/', times_str
    )
    if matches is None:
        raise ValueError('"{0}" does not match date format.'.format(times_str))
    return int(matches.group(1))


def current_time():
    return calendar.timegm(time.gmtime())


def seconds_from_now(time_str):
    return parse_time(time_str) - current_time()
