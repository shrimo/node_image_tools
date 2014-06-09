import sys
from PyQt4.QtCore import Qt, QByteArray
from PyQt4.QtGui import QApplication, QMainWindow, QSplitter, QTabWidget, QTextEdit, QLabel, QImage, QPixmap, QMenu, QCursor

from edd.gui.escene import EScene
from edd.gui.eview import EView

from edd.core.enodehandle import ENodeHandle


from PIL import Image, ImageQt
from nc_lib import *
import numpy
        
class ExampleScene(EScene):

    def __init__(self, view):
        EScene.__init__(self, view)
        self.__control = None
        self.__nodes = {'Blur': BlurNode, 'Size': SizeNode, 'Read': ReadNode, 'Read2': ReadNode2, 'Composite': CompositeNode, 'ColorSpace': ColorSpaceNode, 'Constant': ConstantNode}        
        return

    def getNode(self, name):

        if self.__nodes.has_key(name):
            return self.__nodes[name](name)    

        return None

    def contextMenuEvent(self, event):
        menu = QMenu()
        
        for name in self.__nodes.iterkeys():
            menu.addAction(name)

        view = menu.addAction('View')
        write = menu.addAction('Write')
        quit1 = menu.addAction('Quit')
        ReLoad = menu.addAction('Reload')
        
        action = menu.exec_(QCursor.pos())

        if action == ReLoad:
            #reload(nc_lib)
            print 'Reload'

        if action == quit1:
            print 'Quit'
            sys.exit(app.exec_())

        if action == view:
            viewNode = ViewNode("Viewer")
            self.cwd().addNode(viewNode)
            viewNode.setControl(self.__control)
            print 'add View'

        if action == write:
            writeNode = WriteNode("Write")
            self.cwd().addNode(writeNode)
            writeNode.setControl(self.__control)
            print 'add Write'
        
        node = self.getNode(str(action.text()))

        if node:
            self.cwd().addNode(node)


    def setControl(self, control):
        self.__control = control

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Setup workspace controls
    kWorkspaceSplitter = QSplitter(Qt.Horizontal)
    kWorkspaceSplitter.setObjectName('mainSplitter')

    kResourceTabs = QTabWidget()
    kResourceTabs.setObjectName('kMainTab')
    kResourceTabs.setTabPosition(QTabWidget.South)

    theView = EView()
    theView.Scene = ExampleScene(theView)

    console = QLabel()

    kResourceTabs.addTab(theView, "Node graph")
    kWorkspaceSplitter.addWidget(console)
    kWorkspaceSplitter.addWidget(kResourceTabs)

    theView.Scene.setControl(console)

    window = QMainWindow()
    window.setWindowTitle('Neural composer')
    window.setCentralWidget(kWorkspaceSplitter)

    window.show()
    sys.exit(app.exec_())

