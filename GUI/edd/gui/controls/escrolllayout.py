from PyQt4.QtCore import Qt, QObject, pyqtSignal, QRectF
from PyQt4.QtGui import QPen, QPolygonF, QGraphicsItem, QGraphicsPolygonItem, QGraphicsTextItem, QColor

from edd.gui.utils.edraw import EDraw
from edd.gui.controls.einputfield import EInputField


class EScrollLayout(QGraphicsPolygonItem):

    def __init__(self, parent=None, scene=None):
        super(EScrollLayout, self).__init__(parent, scene)

        #self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setAcceptsHoverEvents(True)

        self.__handleWidth = 500
        self.__handleHeight = 500
        self.__handleRect = QRectF( 0.0 , 0.0 , self.__handleWidth, self.__handleHeight  )

        self.__controls = []

        self.__isDefaultPen = False

        self.__pens = { 0: EDraw.EColor.DefaultLeaveHoverPen, 1: EDraw.EColor.DefaultEnterHoverPen }
        self.setPen(self.__pens[self.__isDefaultPen])

    def setRect(self, qRect):
        self.__handleWidth = qRect.width()
        self.__handleHeight = qRect.height()

        self.setPos( qRect.topLeft().x(), qRect.topLeft().y() )
        self.__handleRect = QRectF( 0.0 , 0.0 , self.__handleWidth, self.__handleHeight  )
        self.updateGeometry()

    def updateGeometry(self):

        for control in self.__controls:
            control.setPos( 0.0, self.boundingRect().height() - control.boundingRect().height() )
            control.Width = self.__handleWidth

        return

    def addControl(self, control):
        #if not isinstance(control, EddControlsGroup): raise AttributeError

        self.__controls.append(control)
        control.Width = self.boundingRect().width()
        control.setParentItem(self)
        control.setFlag(QGraphicsItem.ItemIsMovable, False)

        self.updateGeometry()

    def clear(self):
        [ control.setParentItem(None) for control in self.__controls ]
        self.__controls = []

        self.updateGeometry()

    def shape(self): return QGraphicsItem.shape(self)

    def boundingRect(self):
        return self.__handleRect

    def paint(self, painter, option, widget=None):

        painter.setPen( QPen( QColor( 0, 0, 0, 50 ), 2 , Qt.SolidLine ) )
        #painter.setBrush( QColor( 0, 0, 0, 50 ) )
        painter.drawRect( self.boundingRect() )



