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
        return

    def contextMenuEvent(self, event):
        menu = QMenu()
        
        blur = menu.addAction('Blur')
        size = menu.addAction('Size')
        
        read = menu.addAction('Read')
        read2 = menu.addAction('Read2')

        composite = menu.addAction('Composite')
        
        view = menu.addAction('View')
        colorSpace = menu.addAction('ColorSpace')
        write = menu.addAction('Write')

        quit1 = menu.addAction('Quit')
        
        action = menu.exec_(QCursor.pos())
        if action == quit1:
            print 'Quit'
            sys.exit(app.exec_())
        if action == blur:
            blurNode = BlurNode("Blur")
            self.cwd().addNode(blurNode)
            print 'add Blur'
        if action == size:
            sizeNode = SizeNode("Size")
            self.cwd().addNode(sizeNode)
            print 'add Size'
        if action == read:
            readNode = ReadNode("Read")
            self.cwd().addNode(readNode)
            print 'add Read'

        if action == read2:
            readNode2 = ReadNode2("Read2")
            self.cwd().addNode(readNode2)
            print 'add Read2'
            
        if action == view:
            viewNode = ViewNode("Viewer")
            self.cwd().addNode(viewNode)
            viewNode.setControl(self.__control)
            print 'add View'
        if action == composite:
            compositeNode = CompositeNode("Composite")
            self.cwd().addNode(compositeNode)
            print 'add Composite'
        if action == colorSpace:
            colorSpaceNode = ColorSpaceNode("ColorSpace")
            self.cwd().addNode(colorSpaceNode)
            print 'add Math'

        if action == write:
            writeNode = WriteNode("Write")
            self.cwd().addNode(writeNode)
            writeNode.setControl(self.__control)
            print 'add Write'


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

