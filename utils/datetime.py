import pytz
from datetime import datetime, timedelta


class DateTimeUtil(object):
    """
    Methods support to handle date and time
    """

    @classmethod
    def now(cls, tz_name='Asia/Ho_Chi_Minh'):
        """
        :param tz_name: name of timezone
        :return: current datetime by timezone
        """
        tz = pytz.timezone(tz_name)
        return datetime.now(tz=tz)

    @classmethod
    def today(cls):
        return datetime.date(cls.now())

    @classmethod
    def localize(cls, dt, tz_name='Asia/Ho_Chi_Minh'):
        return dt.astimezone(pytz.timezone(tz_name))

    @classmethod
    def text_to_date(cls, date_text, fmt='%d/%m/%Y', localization=False):
        """ Convert a string to date object by format"""
        dt = datetime.strptime(date_text, fmt)
        return cls.localize(dt) if localization else dt

    @classmethod
    def date_to_text(cls, date_obj, fmt='%d/%m/%Y', localization=False):
        """ Convert a date object to a string by format"""
        if not date_obj:
            return ''

        date_obj = cls.localize(date_obj) if localization else date_obj
        return datetime.strftime(date_obj, fmt)

    @classmethod
    def check_format(cls, date_text, fmt='%d/%m/%Y'):
        """ Check a string has right date format or not"""
        try:
            return cls.text_to_date(date_text, fmt)
        except ValueError:
            return None

    @classmethod
    def is_future(cls, date, forward_seconds=0):
        """ Check a datetime object is future or not"""
        date = cls.localize(date)
        if date > (cls.now() + timedelta(seconds=forward_seconds)):
            return True
        return False

    @classmethod
    def is_past(cls, date, backward_seconds=0):
        """ Check a datetime object is past or not"""
        date = cls.localize(date)
        if (date - timedelta(seconds=backward_seconds)) < cls.now():
            return True
        return False

    @classmethod
    def get_unique_current_time_value(cls, additional_seconds=0):
        now = cls.now()
        if additional_seconds > 0:
            now = now + timedelta(seconds=additional_seconds)
        return cls.date_to_text(now, fmt='%Y%m%d%H%M%S%f', localization=True)
