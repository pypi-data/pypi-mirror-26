# common
import functools

# my
from admin_logs.log import get_record, set_record, RequestRecord


class Log(object):

    def __init__(self, name=None):
        self.old_request = None
        self.name = name

    def __enter__(self):
        self.old_request = get_record()
        record = RequestRecord(name=self.name)
        set_record(record)

    def __exit__(self, exc_type, exc_val, exc_tb):
        record = get_record()
        record.finish_request()

        set_record(self.old_request)


def log(name=None):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            with Log(name=name or func.__name__):
                return func(*args, **kwargs)
        return inner

    return decorator