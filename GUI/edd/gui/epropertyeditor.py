from edd.gui.controls.etextcontrol import ETextControl
from edd.gui.controls.einputfield import EInputField
from edd.gui.controls.eframelayout import EFrameLayout


class EPropertyEditor(EFrameLayout):

    def __init__(self):
        EFrameLayout.__init__(self)

        self.Label = 'Properties'

    def rebuild(self, nodeName, propList):

        self.clear()

        self.Label = '< %s > Properties' % str(nodeName)

        if not len(propList):
            return

        for prop in propList:

            controlGrp = EInputField(prop.Name)

            for x in range(0, 1):
                controlGrp.addControl(ETextControl())

            controlGrp.Width = 200

            self.addControl(controlGrp)

        return