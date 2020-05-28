from datetime import datetime, timedelta


START_TIME = datetime(year=2020, month=5, day=28, hour=17, minute=12, second=5)
STOP_TIME = datetime(year=2021, month=1, day=1)


def set_new_time(start, stop):
    global START_TIME, STOP_TIME
    START_TIME = start
    STOP_TIME = stop


def get_time():
    global START_TIME, STOP_TIME
    return START_TIME, STOP_TIME
