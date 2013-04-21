import uuid
from PyQt4.QtCore import Qt, QRectF, QObject, pyqtSignal
from PyQt4.QtGui import QPainterPath,  QGraphicsTextItem, QStyle, QStyleOptionGraphicsItem, QFont, QFontMetrics, QPolygonF
from edd.gui.utils.edraw import EDraw

class ETextControl(QGraphicsTextItem):

    onValueChanged = pyqtSignal(QGraphicsTextItem)

    def __init__(self, eType = None, parent = None, scene = None):
        super(ETextControl, self).__init__(parent, scene)
        QObject.__init__(self)

        self.__kId = str(uuid.uuid1())
        self.__kType = eType

        self.__sWidth = 100

        self.__isSingleLine = True
        self.__isAdjustable = True
        self.setPlainText('')
        self.setTextWidth( -1 )

        self.setDefaultTextColor(Qt.black)

        #self.__font = QFont('Helvetica', 8, False)
        #self.setFont(self.__font)
        #self.__fn = QFontMetrics(self.__font)


        self.__isDefaultPen = False
        self.__pens = { 0: EDraw.EColor.DefaultLeaveHoverPen, 1: EDraw.EColor.DefaultEnterHoverPen }
        self.setPen(self.__pens[self.__isDefaultPen])

    @property
    def kId(self): return self.__kId

    @property
    def kType(self): return self.__kType

    @property
    def Width(self): return self.boundingRect().width()

    @Width.setter
    def Width(self, width): self.__sWidth = width

    @property
    def Height(self): return self.boundingRect().height()

    @property
    def Value(self): return self.toPlainText()

    @Value.setter
    def Value(self, value):
        self.setPlainText(str( value ))
        self.onValueChanged.emit(self)

    @property
    def Adjustable(self): return self.__isAdjustable

    @Adjustable.setter
    def Adjustable(self, state): self.__isAdjustable = state

    def toggleHighlight(self):
        if self.__isDefaultPen:
            self.__isDefaultPen = False
            self.setPen(self.__pens[self.__isDefaultPen])
        else:
            self.__isDefaultPen = True
            self.setPen(self.__pens[self.__isDefaultPen])

        self.update()

    def setPen(self, pen): self.__pen = pen

    def pen(self): return self.__pen

    def setSingleLine(self, state = True):
        self.__isSingleLine = state

    def hoverEnterEvent(self, mouseEvent):
        self.toggleHighlight()
        QGraphicsTextItem.hoverEnterEvent(self, mouseEvent)

        #self.setTextInteractionFlags(Qt.TextEditorInteraction)

    def hoverLeaveEvent(self, mouseEvent):
        self.toggleHighlight()
        QGraphicsTextItem.hoverLeaveEvent(self, mouseEvent)

        #self.setTextInteractionFlags(Qt.NoTextInteraction)

    def mousePressEvent(self, event):

        if self.textInteractionFlags() == Qt.NoTextInteraction:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)

        QGraphicsTextItem.mousePressEvent(self, event)

    def keyPressEvent(self, keyEvent):

        if keyEvent.key() == Qt.Key_Return or keyEvent.key() == Qt.Key_Enter:
            if self.__isSingleLine:
                self.setTextInteractionFlags(Qt.NoTextInteraction)
            return

        QGraphicsTextItem.keyPressEvent(self, keyEvent)

    def shape(self):
        path = QPainterPath()
        path.addPolygon( EDraw.DefaultPolygon( self.boundingRect().width(), self.boundingRect().height() ) )
        return path

    def boundingRect(self):
        return QRectF( 0.0, 0.0, self.__sWidth, 20)

    def paint(self, painter, option, widget=None):

        painter.setPen(self.pen())
        painter.setBrush( EDraw.EColor.DefaultNodeFillColor )

        style = QStyleOptionGraphicsItem()
        style.state = QStyle.State_None

        painter.drawRoundedRect(self.boundingRect(), 3, 3)

        #painter.translate( self.boundingRect().height() / 6  , 0.0)

        QGraphicsTextItem.paint(self, painter, style, widget)





    
    
    
    
    
    
     