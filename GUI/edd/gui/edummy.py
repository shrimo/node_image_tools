import uuid
import math
from PyQt4.QtCore import pyqtSignal, QPointF, QLineF
from PyQt4.QtGui import QGraphicsObject, QGraphicsItem

from edd.gui.utils.edraw import EDraw
from edd.gui.utils.etransform import ETransform


class EDummy(QGraphicsObject):

    onEditEnd = pyqtSignal(QLineF)
    onPress = pyqtSignal()

    def __init__(self):
        QGraphicsObject.__init__(self)

        self.__uuid = uuid.uuid1()

        #self.setZValue(-0.5)

        self.__polygon = EDraw.Circle(7, 12)
        self.__isSnapMode = False
        self.__snapPoint = QPointF(0.0, 0.0)
        self.__gridSize = 10

        self.__dummyLine = QLineF()
        self.__dummyData = None
        self.__editPointOne = None

        self.__BBTemp = None
        self.__angle = 0.0

    def isEditMode(self):
        if self.__editPointOne:
            return True

        return False

    def toggleEditMode(self):
        if self.__editPointOne is None:
            self.__editPointOne = self.scenePos()
            self.__BBTemp = self.scenePos()
            self.setZValue(2.0)
            self.update()
            return

        self.setZValue(-0.5)

        self.onEditEnd.emit(QLineF(self.__editPointOne, self.scenePos()))

        self.__editPointOne = None
        self.__BBTemp = None

        self.update()

    def setSnapMode(self, snapMode):
        self.__isSnapMode = snapMode

    def setGridSize(self, gridSize):
        self.__gridSize = gridSize

    def setDummyData(self, dummyData):
        self.__dummyData = dummyData

    def getDummyData(self):
        return self.__dummyData

    @property
    def Id(self):
        return self.__uuid

    @property
    def Position(self):
        if self.__isSnapMode:
            return self.__snapPoint / self.__gridSize

        return self.scenePos() / self.__gridSize

    @property
    def Angle(self):
        return self.__angle

    def boundingRect(self):
        tempPoint = self.__snapPoint
        if self.__BBTemp is not None:
            tempPoint = self.__BBTemp

        radius = math.sqrt((self.scenePos().x() - tempPoint.x()) ** 2 + (self.scenePos().y() - tempPoint.y()) ** 2)
        return EDraw.Circle(radius + self.__gridSize / 2, 8).boundingRect().normalized().adjusted(-5, -5, 5, 5)

    def shape(self):
        path = QGraphicsItem.shape(self)
        return path

    def polygon(self):
        return self.__polygon

    def debug(self):
        return self.__dummyLine.p2()

    def dummyLine(self, angle=None, length=None):

        if angle is not None and length is not None:
            pt1 = QLineF(QPointF(0.0, 0.0), QPointF(0.0, 1.0))
            pt1.setAngle(angle)
            pt1.setLength(length + 16)
            self.__dummyLine = pt1
            return

        self.__dummyLine = QLineF()

    def paint(self, painter, option, widget=None):

        painter.setPen(EDraw.EColor.DefaultEnterHoverPen)

        lineX = QLineF(QPointF(self.__gridSize, 0.0), QPointF(0.0, 0.0)).translated(-self.scenePos())
        lineY = QLineF(QPointF(0.0, -self.__gridSize), QPointF(0.0, 0.0)).translated(-self.scenePos())
        painter.drawLines([lineX, lineY])

        self.__snapPoint = QPointF(self.__gridSize * round(self.scenePos().x() / self.__gridSize),
                                   self.__gridSize * round(self.scenePos().y() / self.__gridSize))

        if self.__isSnapMode:
            painter.drawPolygon(self.__polygon.translated(self.__snapPoint - self.scenePos()))

        self.__angle = 0.0

        if self.__editPointOne is not None:
            painter.drawPolygon(EDraw.Circle(20, 24).translated(-(self.scenePos()) + self.__BBTemp))
            painter.drawLine(QLineF(QPointF(-(self.scenePos()) + self.__BBTemp), QPointF(0.0, 0.0)))

            dummyLine = QLineF(QPointF(-(self.scenePos()) + self.__BBTemp), QPointF(0.0, 0.0))

            painter.drawLine(QLineF(ETransform.rotatePoint(20, dummyLine.angle() + 180),
                                    QPointF()).translated(-(self.scenePos()) + self.__BBTemp))
            painter.drawLine(QLineF(ETransform.rotatePoint(20, dummyLine.angle() + 360),
                                    QPointF()).translated(-(self.scenePos()) + self.__BBTemp))

            self.__angle = dummyLine.angle()

        painter.drawPolygon(self.__polygon)
        painter.drawLine(self.__dummyLine)
        #painter.drawRect(self.boundingRect())

    def mousePressEvent(self, event):
        QGraphicsObject.mousePressEvent(self, event)
        self.onPress.emit()





