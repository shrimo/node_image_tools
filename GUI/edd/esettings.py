import sys
import xml.dom.minidom as xml


class ESettings(object):

    EDD_PLUGIN_PATH = 'D:/Devel/Python/edd/plugins'

    def __init__(self):
        sys.path.append(ESettings.EDD_PLUGIN_PATH)

        self.__settingsFile = None
        return

    def __isValid(self, root, tag):
        try:
            if len(root.getElementsByTagName( tag )) > 1:
                raise ValueError('Duplicated Items( <%s> ) in config file "%s"' % (tag, self.__settingsFile))

            return root.getElementsByTagName(tag)

        except Exception, err:
            raise err

    def getElementNodes(self, data):
        return [ x for x in data.childNodes if x.nodeType == xml.Node.ELEMENT_NODE ]

    def process(self, settingsFile):
        self.__settingsFile = settingsFile

        settings = xml.parse(settingsFile).documentElement

        print self.__isValid( settings, 'structure')


if __name__ == "__main__":

    edd = ESettings()

    edd.process("D:/Devel/Python/edd/settings.xml")


