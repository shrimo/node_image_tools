import sys
import uuid
from PyQt4.QtCore import pyqtSignal, QObject

from edd.esettings import ESettings
from edd.utils.efileutils import EFileUtils


class EManager(QObject):

    onSomethingChanged = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.__kId = uuid.uuid1()

        self.__eddSettings = ESettings()
        sys.path.append(ESettings.EDD_PLUGIN_PATH)

        self.__availableNodes = [pluginFileName.strip('.py') for pluginFileName in EFileUtils.getFiles(ESettings.EDD_PLUGIN_PATH, '.py', False)]

        self.__registeredNodes = {}

        self.__genericInput = None
        self.__genericOutput = None

    def loadPlugin(self, nodeName):

        pluginModule = __import__(nodeName, globals(), locals(), [])

        try:
            self.__registeredNodes[pluginModule.nodeCreator().Name] = pluginModule.nodeCreator()
            return pluginModule.nodeCreator()

        except Exception, err:
            print self.__class__.__name__, err
            return None

    def lsPlugins(self, loaded=False):
        if loaded:
            return self.__registeredNodes

        return self.__availableNodes


if __name__ == "__main__":

    manager = EManager()

    for plg in manager.lsPlugins():
        manager.loadPlugin(plg)





