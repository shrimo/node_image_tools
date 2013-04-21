import uuid
from PyQt4.QtCore import pyqtSignal, QObject


class EProxy(type):

    def __new__(mcs, name, bases, dct):
        return type.__new__(mcs, name, bases, dct)
        #return super(EProxy, mcs).__new__(mcs, name, bases, dct)


class EObject(QObject):

    Message = pyqtSignal(QObject)

    def __init__(self, id=None):
        QObject.__init__(self)
        self.__uuid = uuid.uuid1()

        if id is not None and isinstance(id, uuid.UUID):
            self.__uuid = id

        self.__data = None

    @property
    def Id(self):
        return self.__uuid

    def setData(self, data):
        self.__data = data

        return self

    def getData(self):
        return self.__data

    def match(self, eObject):

        #if isinstance(self.__class__, eObject.__class__):
        #    return True

        if not issubclass(eObject.__class__, EObject):
            raise AttributeError

        if self == eObject:
            return True

        return False


















