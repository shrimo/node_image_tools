import uuid
from edd.core.eobject import EObject
from edd.core.eattribute import EAttribute
from edd.core.enodehandle import ENodeHandle
from edd.core.emanager import EManager


class EConnection(EObject):

    def __init__(self, head, tail):
        EObject.__init__(self)

        self.__headAttr = head
        self.__tailAttr = tail

        if head.Type.match(EAttribute.kTypeInput):
            self.__tailAttr = head
            self.__headAttr = tail

        #self.__headAttr.Message.connect(self.__messageFilter)
        #self.__tailAttr.Message.connect(self.__messageFilter)

        self.__tailAttr.Data = self.__headAttr.Data

    def update(self):
        #self.__headAttr.Handle.compute()
        pass

    def __messageFilter(self, message):

        if message.match(EAttribute.kMessageAttributeSet):
            if message.sender().Type.match(EAttribute.kTypeOutput):

                #print "Data set on: <%s.%s>" % (message.sender().Handle.Name, message.sender().Name)
                #print self.__headAttr.Handle.getAttributeById(self.__headAttr.Id).Data
                #self.__tailAttr.Data = self.__headAttr.Handle.getAttributeById(self.__headAttr.Id).Data
                return

        if message.match(EAttribute.kMessageAttributeGet):
            if message.sender().Type.match(EAttribute.kTypeInput):
                result = self.__headAttr.Handle.compute()
                #print result

                if not result:
                    self.__tailAttr.Data = self.__headAttr.Handle.getAttributeById(self.__headAttr.Id).Data

                #print "Data get on: <%s.%s>" % (message.sender().Handle.Name, message.sender().Name)
        return

    @property
    def Head(self):
        return self.__headAttr

    @property
    def Tail(self):
        return self.__tailAttr


class EGraphHandle(EObject):

    kMessageNodeAdded = EObject()
    kMessageNodeRemoved = EObject()
    kMessageNodeUpdate = EObject()

    kMessageEditBegin = EObject()
    kMessageEditEnd = EObject()

    kMessageUnknown = EObject()
    kMessageInternalError = EObject()

    kMessageConnectionMade = EObject()
    kMessageConnectionBroke = EObject()

    def __init__(self):
        EObject.__init__(self)

        self.__nodes = {}
        self.__attributes = {}
        self.__connections = {}

        self.__availableNodes = None
        self.__tAttrId = None

        self.__pluginManager = EManager()

    def __create__(self):
        return

    def __messageFilter(self, message):

        if message.match(ENodeHandle.kMessageAttributeAdded):
            self.__attributes[message.getData().Id] = message.getData()

    def getConnectionFromAttributeId(self, attrId):

        for key, value in self.__connections.iteritems():
            if attrId in [value.Head.Id, value.Tail.Id]:
                return key

        return None

    def getHandleFromId(self, id):
        if not isinstance(id, uuid.UUID):
            raise AttributeError

        if self.__attributes.has_key(id):
            return self.__attributes[id].Handle.Id

        return None

    def ls(self):
        return self.__nodes.values()

    def lsConnected(self):
        return self.__connections

    def select(self, nodeName):
        for handle in self.__nodes.itervalues():
            if nodeName == handle.Name:
                return handle

        return None

    def createNode(self, name=None):

        if name in self.__pluginManager.lsPlugins():
            nodeHandle = self.__pluginManager.loadPlugin(name)
        else:
            nodeHandle = ENodeHandle()
            nodeHandle.Name = name

        self.addNode(nodeHandle)

        return nodeHandle

    def addNode(self, handle):
        if not isinstance(handle, ENodeHandle):
            raise AttributeError

        handle.Message.connect(self.__messageFilter)

        if not handle.Name:
            handle.Name = "EUnknown_%s" % str(len(self.__nodes.keys()))

        self.__nodes[handle.Id] = handle

        for attribute in handle.lsAttributes():
            self.__attributes[attribute.Id] = attribute

        self.Message.emit(self.kMessageNodeAdded.setData(handle))

    def delNode(self, handle):
        self.Message.emit(self.kMessageNodeRemoved.setData(handle))

    def updateNode(self, handle):

        if self.__nodes.has_key(handle.Id):
            self.__nodes[handle.Id] = handle

            self.Message.emit(self.kMessageNodeUpdate)

    def isConnected(self, attribute):
        if not isinstance(attribute, EAttribute):
            raise AttributeError

        return self.__attributes.has_key(attribute.Id)

    def connectAttributes(self, attributeOne, attributeTwo):

        if isinstance(attributeOne, EAttribute):
            attributeOne = attributeOne.Id

        if isinstance(attributeTwo, EAttribute):
            attributeTwo = attributeTwo.Id

        if self.__attributes.has_key(attributeOne) and self.__attributes.has_key(attributeTwo):

            if self.__attributes[attributeOne].Type.match(self.__attributes[attributeTwo].Type):
                self.Message.emit(self.kMessageInternalError.setData(None))
                return False

            if self.__attributes[attributeOne].Handle.match(self.__attributes[attributeTwo].Handle):
                self.Message.emit(self.kMessageInternalError.setData(None))
                return False

            #conn1 = self.getConnectionFromAttributeId(attributeOne)
            #conn2 = self.getConnectionFromAttributeId(attributeTwo)

            #if conn1 and conn2 and conn1 == conn2:
            #    self.Message.emit(self.kMessageInternalError.setData(None))
            #    return False

            if self.__attributes[attributeOne].Type.match(EAttribute.kTypeInput):
                #print self.__attributes[attributeOne].Handle.Name, self.__attributes[attributeOne].Name
                inputAttr = self.__attributes[attributeOne]
            else:
                #print self.__attributes[attributeTwo].Handle.Name, self.__attributes[attributeTwo].Name
                inputAttr = self.__attributes[attributeTwo]

            if inputAttr.isConnected:
                self.disconnectAttribute(inputAttr)

            connection = EConnection(self.__attributes[attributeOne], self.__attributes[attributeTwo])
            self.__connections[connection.Id] = connection

            self.__attributes[attributeOne].isConnected = True
            self.__attributes[attributeTwo].isConnected = True

            connection.update()

            self.Message.emit(self.kMessageConnectionMade.setData([attributeOne, attributeTwo, connection.Id]))
            return True

        return False

    def disconnectAttribute(self, attribute):

        if isinstance(attribute, EAttribute):
            attrId = attribute.Id

        if self.__attributes.has_key(attrId):

            conn = self.getConnectionFromAttributeId(attrId)
            attribute.isConnected = False

            self.Message.emit(self.kMessageConnectionBroke.setData(conn))
            self.__connections.pop(conn, None)

            return True

        return False

    def disconnectAttributes(self, attributeOne, attributeTwo):
        return

    def process(self, data):

        if isinstance(data, list):

            for item in data:
                if self.__connections.has_key(item):
                    attrOne, attrTwo = self.__connections[item].Head, self.__connections[item].Tail

                    if attrOne.Type.match(EAttribute.kTypeInput):
                        self.disconnectAttribute(attrOne)
                    else:
                        self.disconnectAttribute(attrTwo)

            return

        if self.__attributes.has_key(data) and self.__tAttrId is None:
            self.__tAttrId = data
            self.Message.emit(self.kMessageEditBegin.setData(None))
            return

        if self.__tAttrId:

            if self.__attributes.has_key(data):
                self.connectAttributes(self.__tAttrId, data)

            self.__tAttrId = None
            self.Message.emit(self.kMessageEditEnd.setData(None))













