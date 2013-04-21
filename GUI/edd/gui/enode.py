from PyQt4.QtCore import pyqtSignal, Qt, QRectF, QPointF
from PyQt4.QtGui import QFont, QFontMetrics, QColor, QPen, QGraphicsObject, QGraphicsItem

from edd.gui.utils.edraw import EDraw

from edd.core.eobject import EObject
from edd.core.eattribute import EAttribute


class ENode(QGraphicsObject):

    onMove = pyqtSignal()
    onPress = pyqtSignal()

    kGuiPropertyId = EObject()
    kGuiPropertyName = EObject()

    kGuiAttributeId = EObject()
    kGuiAttributeType = EObject()
    kGuiAttributePlug = EObject()
    kGuiAttributeParent = EObject()
    kGuiAttributeParentName = EObject()
    kGuiAttributeLongName = EObject()
    kGuiAttributeShortName = EObject()

    def __init__(self, eNodeHandle):
        QGraphicsObject.__init__(self)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setAcceptsHoverEvents(True)

        self.__isDefaultPen = False

        self.__pen = None
        self.__pens = {0: EDraw.EColor.DefaultLeaveHoverPen, 1: EDraw.EColor.DefaultEnterHoverPen}
        self.setPen(self.__pens[self.__isDefaultPen])

        self.Name = eNodeHandle.Name

        self.__font = QFont('Helvetica', 8, False)
        self.__nodeHandle = eNodeHandle
        self.__nodeHandle.Message.connect(self.__messageFilter)

        self.__attrRect = QRectF(0, 0, 15, 15)

        self.__titleRect = QRectF(0, 0, 135, 20)
        self.__textSpace = QRectF(self.__attrRect.width() + self.pen().width(), 0.0,
                                  (self.__titleRect.width() - self.__attrRect.width() * 2 - self.pen().width() * 2) / 2,
                                  self.__attrRect.height())

        self.__attributes = {}
        self.__properties = {}

        self.__out_attr_step = self.__titleRect.height() + self.pen().width()
        self.__in_attr_step = self.__titleRect.height() + self.pen().width()

        self.__buildAttributes()

        self.__height = max([self.__in_attr_step, self.__out_attr_step])

    def __messageFilter(self, message):
        if message.match(self.__nodeHandle.kMessageAttributeAdded):
            self.__buildAttribute(message.getData())

    def __getAttrShortName(self, attributeName):
        fm = QFontMetrics(self.__font)

        shortName = ''

        if fm.width(attributeName) > self.__textSpace.width():

            for x in range(len(attributeName) + 1):
                if fm.width(shortName) > int(self.__textSpace.width()) - 10:
                    return shortName

                shortName = attributeName[:x] + '...'

        return attributeName

    def __getAttributePosition(self, attrType):

        attr_x_pos = 0

        if attrType.match(EAttribute.kTypeOutput):

            attr_x_pos = self.__titleRect.width() - self.__attrRect.width()
            rect = self.__attrRect.translated(QPointF(attr_x_pos, self.__out_attr_step))

            point = QPointF((rect.topRight() + rect.bottomRight()) / 2)
            point.setX(point.x() + self.pen().width() * 2)

            self.__out_attr_step += self.__attrRect.width() + self.pen().width()

            return [rect, point]

        rect = self.__attrRect.translated(QPointF(attr_x_pos, self.__in_attr_step))
        point = QPointF((rect.topLeft() + rect.bottomLeft()) / 2)
        point.setX(point.x() - self.pen().width() * 2)

        self.__in_attr_step += self.__attrRect.width() + self.pen().width()

        return [rect, point]

    def __buildAttribute(self, attribute):

        if attribute.Type.match(EAttribute.kTypeProperty):
            self.__properties[attribute.Id] = dict({self.kGuiPropertyId: attribute.Id,
                                                    self.kGuiPropertyName: attribute.Name})
            return

        data = self.__getAttributePosition(attribute.Type)

        self.__attributes[data[0]] = dict({self.kGuiAttributeId: attribute.Id,
                                           self.kGuiAttributeType: attribute.Type,
                                           self.kGuiAttributeParent: self,
                                           self.kGuiAttributeParentName: self.__nodeHandle.Name,
                                           self.kGuiAttributePlug: data[1],
                                           self.kGuiAttributeLongName: attribute.Name,
                                           self.kGuiAttributeShortName: self.__getAttrShortName(attribute.Name)})

        self.__height = max([self.__in_attr_step, self.__out_attr_step])

        self.update()
        self.onMove.emit()

    def __buildAttributes(self):

        for eddAttr in self.__nodeHandle.lsAttributes():
            self.__buildAttribute(eddAttr)

    def __toggleHighlight(self):
        if self.__isDefaultPen:
            self.__isDefaultPen = False
            self.setPen(self.__pens[self.__isDefaultPen])
            #self.setZValue(0.0)
            return

        self.__isDefaultPen = True
        self.setPen(self.__pens[self.__isDefaultPen])
        #self.setZValue(-2.0)

    @property
    def Id(self):
        return self.__nodeHandle.Id

    def pen(self):
        return self.__pen

    def setPen(self, pen):
        if not isinstance(pen, QPen):
            raise AttributeError

        self.__pen = pen

    @property
    def Handle(self):
        return self.__nodeHandle

    @property
    def Properties(self):
        return self.__properties

    def mapFromPoint(self, QPoint):

        for attrRect, attrValues in self.__attributes.iteritems():
            if attrRect.contains(self.mapFromScene(QPoint)):
                return attrValues[self.kGuiAttributeId]

        return self.__nodeHandle.Id

    def mapFromId(self, attrId):

        for attrValue in self.__attributes.itervalues():
            if attrValue[self.kGuiAttributeId] == attrId:
                return attrValue

        return None

    def hoverEnterEvent(self, mouseEvent):
        QGraphicsObject.hoverEnterEvent(self, mouseEvent)
        self.__toggleHighlight()

    def hoverMoveEvent(self, mouseEvent):
        QGraphicsObject.hoverMoveEvent(self, mouseEvent)

    def hoverLeaveEvent(self, mouseEvent):
        QGraphicsObject.hoverLeaveEvent(self, mouseEvent)
        self.__toggleHighlight()

    def mousePressEvent(self, mouseEvent):
        QGraphicsObject.mousePressEvent(self, mouseEvent)

        #if mouseEvent.button() == Qt.RightButton:
        #print self.mapFromPoint(mouseEvent.scenePos())
        self.onPress.emit()

    def mouseDoubleClickEvent(self, mouseEvent):
        QGraphicsObject.mouseDoubleClickEvent(self, mouseEvent)

        #self.__nodeHandle.compute()

    def mouseMoveEvent(self, mouseEvent):
        QGraphicsObject.mouseMoveEvent(self, mouseEvent)
        self.onMove.emit()

    def boundingRect(self):
        extra = self.pen().width()
        return self.__titleRect.normalized().adjusted(-extra, -extra, extra,
                                                      (self.__height - self.__titleRect.height()) + extra)

    def shape(self):
        return QGraphicsItem.shape(self)

    def paint(self, painter, option, widget=None):

        painter.setBrush(EDraw.EColor.DefaultNodeFillColor)

        painter.setPen(self.pen())
        painter.drawRect(self.boundingRect())

        painter.setPen(Qt.NoPen)

        painter.setBrush(EDraw.EColor.DefaultTitleColor)
        painter.drawRect(self.__titleRect)

        painter.setPen(EDraw.EColor.DefaultTitleTextColor)
        painter.drawText(self.__titleRect, Qt.AlignCenter, self.Name)

        painter.setPen(Qt.NoPen)
        painter.setBrush(EDraw.EColor.DefaultAttributeFillColor)

        for rect in self.__attributes.iterkeys():
            painter.drawRect(rect)

        painter.setBrush(Qt.darkGray)
        for rect in self.__attributes.iterkeys():
            painter.drawPolygon(EDraw.Circle(rect.height() / 3, 3).translated(rect.center()))

        painter.setPen(QPen(QColor(43, 43, 43), 1.0, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)

        for attrRect, attrValues in self.__attributes.iteritems():

            attrNameRect = self.__textSpace.translated(attrRect.topLeft())
            align = Qt.AlignLeft

            if attrRect.topLeft().x() > 0:
                attrNameRect = self.__textSpace.translated(
                    QPointF((self.__titleRect.width() / 2) - (attrRect.width() + self.pen().width()),
                            attrRect.topLeft().y()))

                align = Qt.AlignRight

            painter.drawText(attrNameRect, align,  attrValues[self.kGuiAttributeShortName])



