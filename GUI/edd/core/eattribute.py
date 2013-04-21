from edd.core.eobject import EObject


class EAttribute(EObject):

    """

    .. glossary::

        kTypeInput
        kTypeOutput

    """

    kTypeInput = EObject()
    kTypeOutput = EObject()
    kTypeProperty = EObject()

    kMessageAttributeSet = EObject()
    kMessageAttributeGet = EObject()
    kMessageAttributeRenamed = EObject()

    def __init__(self):
        EObject.__init__(self)

        self.__type = None
        self.__isConnected = False

        self.__attrName = None
        self.__attrData = None
        self.__handle = None

    def create(self, attributeType, attributeName, attributeData=None):

        self.__type = attributeType
        self.__attrName = attributeName
        self.__attrData = attributeData

        return self

    @property
    def Type(self):
        """

           :param flab_nickers: a series of under garments to process
           :param has_polka_dots: default False
           :param needs_pressing: default False, Whether the list of garments should all be pressed
           """
        return self.__type

    @property
    def Name(self):
        return self.__attrName

    @Name.setter
    def Name(self, name):
        self.__attrName = name

        self.Message.emit(self.kMessageAttributeRenamed)

    @property
    def Handle(self):
        return self.__handle

    @Handle.setter
    def Handle(self, handle):
        self.__handle = handle

    @property
    def Data(self):
        self.Message.emit(self.kMessageAttributeGet)

        return self.__attrData

    @Data.setter
    def Data(self, attrData):
        self.__attrData = attrData

        self.Message.emit(self.kMessageAttributeSet)

    def isInput(self):
        if self.__type == self.kTypeInput:
            return True

        return False

    def isOutput(self):
        if self.__type == self.kTypeOutput:
            return True

        return False

    @property
    def isArray(self):
        """Comment.

        .. note::

            print public_fn_with_googley_docstring(name='foo', state=None)

        """
        return None

    @isArray.setter
    def isArray(self, state):
        return

    @property
    def isConnected(self):
        """This function does something.

        Args:
           name (str):  The name to use.

        Kwargs:
           state (bool): Current state to be in.

        Returns:
           int.  The return code::

              0 -- Success!

        A really great idea.  A way you might use me is

        >>> print public_fn_with_googley_docstring(name='foo', state=None)
        0

        .. warning::

            BTW, this always returns 0.  **NEVER** use with :class:`MyPublicClass`.

        """
        return self.__isConnected

    @isConnected.setter
    def isConnected(self, state):
        self.__isConnected = state

    def clear(self):
        self.__attrData = None







