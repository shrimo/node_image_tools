import math
from PyQt4.QtCore import Qt, QSizeF, QPointF, QLineF, QRectF
from PyQt4.QtGui import QColor, QPen, QGraphicsObject, QPainterPath

from edd.core.eattribute import EAttribute
from edd.gui.enode import ENode


class EEdge(QGraphicsObject):
    def __init__(self, head, tail, uuid):
        QGraphicsObject.__init__(self)

        if not issubclass(head.__class__, dict) and not isinstance(tail.__class__, dict):
            raise AttributeError

        self.setZValue(0.0)

        self.__kId = uuid
        self.__head = head
        self.__tail = tail

        self.__path = QPainterPath()

        if head[ENode.kGuiAttributeType].match(EAttribute.kTypeInput):
            self.__head = tail
            self.__tail = head

        self.__head[ENode.kGuiAttributeParent].onMove.connect(self.update)
        self.__tail[ENode.kGuiAttributeParent].onMove.connect(self.update)

        self.__headPoint = QPointF(0.0, 0.0)
        self.__tailPoint = QPointF(0.0, 0.0)

        self.__pen = QPen(QColor(43, 43, 43), 2, Qt.SolidLine)

        self.update()

    @property
    def Id(self):
        return self.__kId

    @property
    def Line(self):
        return QLineF(self.__headPoint, self.__tailPoint)

    @property
    def Head(self):
        return self.__head

    @property
    def Tail(self):
        return self.__tail

    def pen(self):
        return self.__pen

    def setPen(self, pen):
        if not isinstance(pen, QPen):
            raise AttributeError

        self.__pen = pen

    def update(self):

        QGraphicsObject.prepareGeometryChange(self)

        self.__headPoint = self.mapFromItem(self.__head[ENode.kGuiAttributeParent],
                                            self.__head[ENode.kGuiAttributePlug])

        self.__tailPoint = self.mapFromItem(self.__tail[ENode.kGuiAttributeParent],
                                            self.__tail[ENode.kGuiAttributePlug])

        self.__headOffsetLine = QLineF(self.__headPoint, QPointF(self.__headPoint.x() + 15, self.__headPoint.y()))
        self.__tailOffsetLine = QLineF(self.__tailPoint, QPointF(self.__tailPoint.x() - 15, self.__tailPoint.y()))

        line = QLineF(self.__headPoint, self.__tailPoint)
        self.__line = line

    def boundingRect(self):
        extra = (self.pen().width() * 64) / 2
        return QRectF(self.__line.p1(),
                      QSizeF(self.__line.p2().x() - self.__line.p1().x(),
                             self.__line.p2().y() - self.__line.p1().y())).normalized().adjusted(-extra,
                                                                                                 -extra,
                                                                                                 extra,
                                                                                                 extra)

    def shape(self):
        #return QGraphicsObject.shape(self)
        return QPainterPath(self.__path)

    def drawPath(self, startPoint, endPoint):
        path = QPainterPath()

        one = (QPointF(endPoint.x(), startPoint.y()) + startPoint) / 2
        two = (QPointF(startPoint.x(), endPoint.y()) + endPoint) / 2

        path.moveTo(startPoint)

        angle = math.pi / 2
        bLine1 = QLineF()
        bLine1.setP1(startPoint)

        if startPoint.x() > endPoint.x():
            dist = startPoint.x() - endPoint.x()
            one = (bLine1.p1() + QPointF(math.sin(angle) * dist,  math.cos(angle) * dist))
            bLine1.setP1(endPoint)
            two = (bLine1.p1() + QPointF(math.sin(angle) * dist,  math.cos(angle) * dist))

        path.cubicTo(one, two,  endPoint)

        self.__path = path
        return path, QLineF(one, two)

    def paint(self, painter, option, widget=None):

        painter.setPen(self.pen())

        headCenter = self.mapFromItem(self.__head[ENode.kGuiAttributeParent],
                                      self.__head[ENode.kGuiAttributeParent].boundingRect().center())

        tailCenter = self.mapFromItem(self.__tail[ENode.kGuiAttributeParent],
                                      self.__tail[ENode.kGuiAttributeParent].boundingRect().center())

        centerPoint = QLineF(headCenter, tailCenter).pointAt(0.5)

        centerPoint.setX(self.__headOffsetLine.p2().x())
        lineFromHead = QLineF(self.__headOffsetLine.p2(), centerPoint)
        centerPoint.setX(self.__tailOffsetLine.p2().x())
        lineFromTail = QLineF(self.__tailOffsetLine.p2(), centerPoint)

        painter.drawPath(self.drawPath(self.__headOffsetLine.p1(), self.__tailOffsetLine.p1())[0])

        #painter.drawLines([self.__headOffsetLine, self.__tailOffsetLine])
        #painter.drawLines([lineFromHead, lineFromTail, QLineF(lineFromTail.pointAt(1.0), lineFromHead.pointAt(1.0))])

