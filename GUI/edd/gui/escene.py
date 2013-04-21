from PyQt4.QtCore import Qt, QPointF, QLineF, QRectF
from PyQt4.QtGui import QPen, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsLineItem

from edd.core.egraphhandle import EGraphHandle

from edd.gui.utils.edraw import EDraw
from edd.gui.edummy import EDummy
from edd.gui.eedge import EEdge
from edd.gui.enode import ENode
from edd.gui.epropertyeditor import EPropertyEditor


class ESceneSelection(QGraphicsItem):

    def __init__(self):
        QGraphicsItem.__init__(self)

        self.__selected = None
        self.setZValue(3.0)

        self.__mark = EDraw.Circle(10, 3, 90).translated(QPointF(0.0, -12.0))

        self.__pen = EDraw.EColor.DefaultEnterHoverPen

    def __getSelectedCenter(self):
        tLine = QLineF(self.__selected.mapToScene(self.__selected.boundingRect().topLeft()),
                       self.__selected.mapToScene(self.__selected.boundingRect().topRight()))

        return tLine.pointAt(0.5)

    def __getSelectionPolygon(self):
        return

    @property
    def Item(self):
        return self.__selected

    @Item.setter
    def Item(self, newItem):
        self.__selected = newItem

    def boundingRect(self):
        if self.__selected is not None:
            extra = self.__pen.width()
            return self.__mark.boundingRect().adjusted(-extra, -extra, extra, extra).translated(self.__getSelectedCenter())

        return QRectF()

    def shape(self):
        return QGraphicsItem.shape(self)

    def paint(self, painter, option, widget=None):

        if self.__selected is not None:
            painter.setPen(self.__pen)
            painter.setBrush(EDraw.EColor.DefaultTitleColor)
            painter.drawPolygon(self.__mark.translated(self.__getSelectedCenter()))


class EScene(QGraphicsScene):

    def __init__(self, view=None, parent=None):
        QGraphicsScene.__init__(self, parent)

        if view is None:
            raise AttributeError

        self.__view = view
        self.__create__()

    def __create__(self):

        self.__gridSize = 35

        self.__isGridActive = True
        self.__isAltModifier = False
        self.__isControlModifier = False
        self.__isNodePressed = False

        self.__kDummy = EDummy()
        self.__kDummy.setGridSize(self.__gridSize)
        self.__kDummy.onPress.connect(self.__onNodePressed)
        self.__kDummy.onEditEnd.connect(self.__onDummyEdit)

        self.addItem(self.__kDummy)

        self.__kSelected = ESceneSelection()

        self.addItem(self.__kSelected)

        self.__kCutLine = QGraphicsLineItem()
        self.__kCutLine.hide()

        self.addItem(self.__kCutLine)

        self.__nodes = {}
        self.__connections = {}

        self.__graphHandle = EGraphHandle()
        self.__graphHandle.Message.connect(self.__messageFilter)

        self.__propEditor = EPropertyEditor()
        self.addItem(self.__propEditor)

    def __isNode(self, EObject):
        return isinstance(EObject, ENode)

    def __isEdge(self, EObject):
        return isinstance(EObject, EEdge)

    def __onNodePressed(self):

        if self.__isNode(self.sender()):
            self.__graphHandle.process(self.sender().mapFromPoint(self.__kDummy.scenePos()))
            return

        if not self.__kDummy.isEditMode():
            self.__graphHandle.process(self.__kDummy.Id)

    def __onDummyEdit(self, line):

        if self.__isNode(self.itemAt(line.p1())) and self.__isNode(self.itemAt(line.p2())):
            return

        self.__kCutLine.setLine(line)

        result = []

        for item in self.__kCutLine.collidingItems():
            if isinstance(item, EEdge):

                if self.__kCutLine.collidesWithPath(item.shape()):
                    result.append(item.Id)

        self.__graphHandle.process(result)

    def __getDataFromId(self, theId):
        handle = self.__graphHandle.getHandleFromId(theId)
        if handle:
            return self.__nodes[handle].mapFromId(theId)

        return None

    def __messageFilter(self, message):

        if message.match(EGraphHandle.kMessageEditBegin):
            self.__kDummy.toggleEditMode()
            return

        if message.match(EGraphHandle.kMessageEditEnd):
            if self.__kDummy.isEditMode():
                self.__kDummy.toggleEditMode()
            return

        if message.match(EGraphHandle.kMessageNodeAdded):
            self.addItem(ENode(message.getData()))
            return

        if message.match(EGraphHandle.kMessageNodeRemoved):
            return

        if message.match(EGraphHandle.kMessageConnectionMade):

            dataOne = self.__getDataFromId(message.getData()[0])
            dataTwo = self.__getDataFromId(message.getData()[1])

            if dataOne and dataTwo:

                conn = EEdge(dataOne, dataTwo, message.getData()[2])
                self.__connections[conn.Id] = conn
                self.addItem(conn)

                headData = conn.Head
                tailData = conn.Tail

                print 'Result: Connected %s.%s to %s.%s' % (headData[ENode.kGuiAttributeParentName],
                                                            headData[ENode.kGuiAttributeLongName],
                                                            tailData[ENode.kGuiAttributeParentName],
                                                            tailData[ENode.kGuiAttributeLongName])

            return

        if message.match(EGraphHandle.kMessageConnectionBroke):
            if message.getData() in self.__connections.keys():
                self.removeItem(self.__connections[message.getData()])

                self.__connections.pop(message.getData(), None)

                self.update()

                #print "Disconnected..."

            return

        if message.match(EGraphHandle.kMessageUnknown) or message.match(EGraphHandle.kMessageInternalError):
            print 'Result: No event <%s>' % message.getData()
            if self.__kDummy.isEditMode():
                self.__kDummy.toggleEditMode()
                self.update()

    def build(self, handle):
        if not isinstance(handle, EGraphHandle):
            raise AttributeError

    def addItem(self, QGraphicsItem):

        if self.__isNode(QGraphicsItem):
            QGraphicsItem.setZValue(1.0)
            QGraphicsItem.onPress.connect(self.__onNodePressed)

            self.__nodes[QGraphicsItem.Id] = QGraphicsItem

        QGraphicsScene.addItem(self, QGraphicsItem)

    def cwd(self):
        return self.__graphHandle

    def ls(self, sl=False):
        if sl:
            return self.__kSelected

        return self.__nodes.values()

    def drawBackground(self, painter, rect):
        self.update()

        if self.__isGridActive:

            painter.setPen(Qt.NoPen)
            painter.fillRect(rect, Qt.lightGray)

            left = int(rect.left()) - (int(rect.left()) % self.__gridSize)
            top = int(rect.top()) - (int(rect.top()) % self.__gridSize)
            lines = []
            right = int(rect.right())
            bottom = int(rect.bottom())
            for x in range(left, right, self.__gridSize):
                lines.append(QLineF(x, rect.top(), x, rect.bottom()))
            for y in range(top, bottom, self.__gridSize):
                lines.append(QLineF(rect.left(), y, rect.right(), y))

            painter.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
            painter.drawLines(lines)
            return

        painter.fillRect(rect, Qt.lightGray)

    def mouseMoveEvent(self, mouseEvent):
        QGraphicsScene.mouseMoveEvent(self, mouseEvent)

        self.__kDummy.setPos(mouseEvent.scenePos())

        self.update()

    def mousePressEvent(self, mouseEvent):
        QGraphicsScene.mousePressEvent(self, mouseEvent)

        item = self.itemAt(mouseEvent.scenePos())

        if self.__isControlModifier:
            return

        if self.__isNode(item):
            #print item.Properties
            self.__kSelected.Item = item
            self.__propEditor.rebuild(self.__kSelected.Item.Handle.Name, self.__kSelected.Item.Handle.lsProperties())

        elif isinstance(item, EDummy):
            self.__kSelected.Item = None
            self.__propEditor.rebuild("", [])

        if mouseEvent.button() == Qt.RightButton:
            if self.__isNode(self.itemAt(mouseEvent.scenePos())):
                self.__isNodePressed = True
                return

            self.__kDummy.toggleEditMode()

    def mouseReleaseEvent(self, mouseEvent):

        if mouseEvent.button() == Qt.RightButton:
            if self.__isNodePressed:
                self.__isNodePressed = False
                return

            self.__kDummy.toggleEditMode()

        self.update()

        QGraphicsScene.mouseReleaseEvent(self, mouseEvent)

    def keyPressEvent(self, keyEvent):
        QGraphicsScene.keyPressEvent(self, keyEvent)

        if keyEvent.key() == Qt.Key_Control:
            self.__view.setDragMode(QGraphicsView.ScrollHandDrag)
            self.__isControlModifier = True

        if keyEvent.key() == Qt.Key_Alt:
            self.__isAltModifier = True
            self.__previousSelectedNode = None

        if keyEvent.key() == 88:
            self.__kDummy.setSnapMode(True)

    def keyReleaseEvent(self, keyEvent):
        QGraphicsScene.keyReleaseEvent(self, keyEvent)

        if keyEvent.key() == Qt.Key_Control:
            self.__view.setDragMode(QGraphicsView.NoDrag)
            self.__isControlModifier = False

        if keyEvent.key() == Qt.Key_Alt:
            self.__isAltModifier = False
            self.__previousSelectedNode = None

        if keyEvent.key() == 88:
            self.__kDummy.setSnapMode(False)


        
        

