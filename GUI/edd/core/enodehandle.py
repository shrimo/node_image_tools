from edd.core.eobject import EObject
from edd.core.eattribute import EAttribute


#TODO: Keep order ;)

class ENodeHandle(EObject):

    # Messages
    kMessageAttributeMarked = EObject()
    kMessageAttributeAdded = EObject()
    kMessageAttributeRemoved = EObject()

    def __init__(self, name=None):
        EObject.__init__(self)
        self.Name = name
        self.IsStatic = False

        self.__attributes = {}
        self.__connections = {}
        return

    def __messageFilter(self, message):

        if message.match(EAttribute.kMessageAttributeSet) and self.IsStatic:
            self.compute()
            return

        if message.match(EAttribute.kMessageAttributeGet):
            if message.sender().Type.match(EAttribute.kTypeOutput):
                self.compute()

    def compute(self):
        return None

    def hasAttribute(self, eAttribute):
        return

    def hasAttributeOfType(self, eAttributeType):
        return

    def addInputAttribute(self, attrName, attrValue=None):
        attr = EAttribute().create(EAttribute.kTypeInput, attrName, attrValue)

        self.addAttribute(attr)
        return attr

    def addOutputAttribute(self, attrName, attrValue=None):
        attr = EAttribute().create(EAttribute.kTypeOutput, attrName, attrValue)

        self.addAttribute(attr)
        return attr

    def addProperty(self, propName, propValue):
        attr = EAttribute().create(EAttribute.kTypeProperty, propName, propValue)
        self.addAttribute(attr)
        return attr

    def addAttribute(self, eAttribute):
        if not isinstance(eAttribute, EAttribute):
            raise

        result = self.getAttributeByName(eAttribute.Name)
        if len(result):
            if len(result) > 1 or result[0].Type.match(eAttribute.Type):
                raise AttributeError("Attribute name is not unique! <%s.%s>" % (self.Name, eAttribute.Name))

        self.__attributes[eAttribute.Id] = eAttribute
        eAttribute.Handle = self

        eAttribute.Message.connect(self.__messageFilter)

        self.Message.emit(self.kMessageAttributeAdded.setData(eAttribute))

    def delAttribute(self, attributeName):
        attr = self.getAttributeByName(attributeName)
        if attr is not None:
            self.__attributes.pop(attr.Id, None)
            self.Message.emit(ENodeHandle.kMessageAttributeRemoved)

    def lsAttributes(self, eType=None):

        if eType is not None:
            if isinstance(eType, list):
                return [eAttribute for eAttribute in self.__attributes.itervalues() if
                        eAttribute.Type in eType]

            return [eAttribute for eAttribute in self.__attributes.itervalues() if eAttribute.Type.match(eType)]

        return [eAttribute for eAttribute in self.__attributes.itervalues()]

    def lsProperties(self):
        return self.lsAttributes(EAttribute.kTypeProperty)

    def getAttribute(self, eAttribute):
        if not isinstance(eAttribute, EAttribute):
            raise AttributeError

        return self.getAttributeById(eAttribute.Id)

    def getAttributeById(self, attributeId):
        if self.__attributes.has_key(attributeId):
            return self.__attributes[attributeId]

        return None

    def getAttributeByName(self, attributeName):
        result = []
        for attr in self.__attributes.itervalues():
            if attributeName == attr.Name:
                result.append(attr)

        return result

    def addConnection(self, connection):
        return

    def delConnection(self, connection):
        return

    def getConnections(self):
        return self.__connections





        




























