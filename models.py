from abc import ABCMeta, abstractmethod


class AbstractModel:
    __metaclass__ = ABCMeta


class DbField:
    length = None


class CharField(DbField):

    def __init__(self, length=100):
        self.length = length

    def get_type(self):
        return ' varchar(' + str(self.length) + ')'


class IntegerField(DbField):

    def __init__(self):
        self.length = 10

    def get_type(self):
        return ' int(' + str(self.length) + ')'


class FloatField(DbField):

    def __init__(self):
        self.length = 10

    def get_type(self):
        return ' float(' + str(self.length) + ')'


class BooleanField(DbField):

    def __init__(self):
        pass

    @staticmethod
    def get_type():
        return ' boolean'
