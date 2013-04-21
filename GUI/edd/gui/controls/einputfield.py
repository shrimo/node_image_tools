import uuid
from PyQt4.QtCore import Qt, QRectF
from PyQt4.QtGui import QPolygonF, QGraphicsItem, QGraphicsPolygonItem, QGraphicsTextItem

from edd.gui.utils.edraw import EDraw


class EInputField(QGraphicsPolygonItem):

    def __init__(self, label=None, parent=None, scene=None):
        super(EInputField, self).__init__(parent, scene)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setAcceptsHoverEvents(True)

        self.__kId = uuid.uuid1()
        self.__name = QGraphicsTextItem()
        self.__name.setPlainText(str("  %s" % label).capitalize())

        self.__sWidth = 300
        self.__sHeight = 20
        self.__sExtra = 8
        self.__controlsOffset = 5

        self.__isDefaultPen = False

        self.__pens = {0: EDraw.EColor.DefaultLeaveHoverPen, 1: EDraw.EColor.DefaultEnterHoverPen}
        self.setPen(self.__pens[self.__isDefaultPen])

        self.__shapeRect = QRectF(0, 0, self.__sWidth, self.__sHeight)
        self.__controls = []

    def updateGeometry(self):

        adjustableControls = [control for control in self.__controls if control.Adjustable]

        if len(adjustableControls):
            fixedControlsBounds = self.__name.boundingRect().width()
            fixedControlsBounds += sum(
                map(int, [control.boundingRect().width() for control in self.__controls if not control.Adjustable]))

            adjustableControlsWidth = int((self.__sWidth - fixedControlsBounds)) / len(adjustableControls)

        step = self.__name.boundingRect().width()

        for control in self.__controls:
            if control.Adjustable:
                control.Width = adjustableControlsWidth - self.__controlsOffset

            control.setPos(step, 0.0)
            step += control.boundingRect().width() + self.__controlsOffset

        self.__shapeRect = QRectF(0, -(self.__sExtra / 2), self.__sWidth,
                                  max([control.Height for control in self.__controls]) + self.__sExtra)

    @property
    def kId(self):
        return self.__kId

    @property
    def Label(self):
        return self.__name

    @Label.setter
    def Label(self, label):
        self.__name = label

    @property
    def Width(self):
        return self.__sWidth

    @Width.setter
    def Width(self, width):
        self.__sWidth = width
        self.updateGeometry()

    @property
    def Height(self):
        return self.__sHeight

    @property
    def Controls(self):
        return self.__controls

    def addControl(self, control):
        control.setParentItem(self)
        self.__controls.append(control)
        self.updateGeometry()

    def toggleHighlight(self):
        if self.__isDefaultPen:
            self.__isDefaultPen = False
            self.setPen(self.__pens[self.__isDefaultPen])
            return

        self.__isDefaultPen = True
        self.setPen(self.__pens[self.__isDefaultPen])

    def hoverEnterEvent(self, mouseEvent):
        QGraphicsPolygonItem.hoverEnterEvent(self, mouseEvent)
        self.toggleHighlight()

    def hoverLeaveEvent(self, mouseEvent):
        QGraphicsPolygonItem.hoverLeaveEvent(self, mouseEvent)
        self.toggleHighlight()

    def shape(self):
        return QGraphicsItem.shape(self)

    def boundingRect(self):
        return self.__shapeRect

    def paint(self, painter, option, widget=None):

        painter.setPen(self.pen())
        #painter.setBrush(EDraw.EColor.LinearGradient(self.boundingRect(), Qt.darkGray))

        painter.setBrush(EDraw.EColor.DefaultTitleColor)

        #painter.drawPolygon(QPolygonF(self.boundingRect()))
        painter.drawRoundedRect(self.boundingRect(), 3, 3)

        painter.setPen(EDraw.EColor.DefaultTitleTextColor)

        r = QRectF(0.0, -(self.__sExtra / 2), self.__name.boundingRect().width(), self.boundingRect().height())
        painter.drawText(r, Qt.AlignRight | Qt.AlignCenter, "%s: " % self.__name.toPlainText())








