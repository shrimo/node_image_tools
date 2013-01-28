import sys
from PyQt4 import QtCore, QtGui

from node_lib import *

import Image
import numpy

class Viewport(QtGui.QWidget):
    def __init__(self):
        super(Viewport, self).__init__()

        self.points = []
        self.x = 0
        self.y = 0
        self.StartStop=0

        self.img=Image.new("RGB", (400, 200))
        self.Nimg = numpy.array(self.img)
        self.WIDTH, self.HEIGHT = self.img.size
        self.init_ui()

    def init_ui(self):
        btnFile = QtGui.QPushButton("File", self)
        self.btnStart = QtGui.QPushButton("Start", self)
        self.btnStart.setCheckable(True)
        btnRedraw = QtGui.QPushButton("Redraw", self)

        NodeButton = QtGui.QPushButton("Node")
        NodeMenu = QtGui.QMenu()
        NodeMenu.addAction("&Blur",self.BlurClicked)
        NodeMenu.addAction("&Sharpen",self.SharpenClicked)
        NodeMenu.addAction("&Invert",self.InvertClicked)
        NodeMenu.addAction("&Rotate",self.RotateClicked)
        NodeButton.setMenu(NodeMenu)
        ColorAction = NodeMenu.addAction("&Color")
        ColorMenu = QtGui.QMenu()
        ColorMenu.addAction("&Bright",self.BrightClicked)
        ColorMenu.addAction("&Contrast",self.ContrastClicked)
        ColorAction.setMenu(ColorMenu)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(btnFile)
        hbox.addWidget(self.btnStart)
        hbox.addWidget(btnRedraw)
        hbox.addWidget(NodeButton)
        hbox.addStretch(1)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        btnFile.clicked.connect(self.FileClicked)
        self.btnStart.clicked[bool].connect(self.StartClicked)
        btnRedraw.clicked.connect(self.RedrawClicked)

        self.setGeometry(300, 300, self.WIDTH, self.HEIGHT+50)
        self.setWindowTitle('Node viewport')
        self.show()

    def StartClicked(self):
        if (self.StartStop==0):
            self.btnStart.setText('Stop')
            self._timerId = self.startTimer(0)
            self.StartStop=1
            return

        if (self.StartStop==1):
            self.btnStart.setText('Start')
            if self._timerId is not None:
                self.killTimer(self._timerId)
            self._generator = None
            self._timerId = None
            self.StartStop=0
            return

    def timerEvent(self, e):
        if len(self.points) >= self.WIDTH*self.HEIGHT:
            self.killTimer(0)
            self.btnStart.setText('Start')
            self.StartStop=0
            return
        if len(self.points) < self.WIDTH*self.HEIGHT:
            for self.x in range(self.WIDTH):
                rgb=self.Nimg[self.y,self.x,:]
                self.points.append((
                self.x,
                self.y,
                QtGui.QColor(rgb[0],rgb[1],rgb[2]),
                ))
            self.update()
            self.x=0
            self.y+=1;


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)

        for point in self.points:

            qp.setPen(point[2])
            qp.drawPoint(point[0], point[1])

        qp.end()

    def FileClicked(self, e):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        self.img=Image.open(str(fname))
        self.Nimg = numpy.array(self.img)

        self.WIDTH, self.HEIGHT = self.img.size
        self.setGeometry(300, 300, self.WIDTH, self.HEIGHT+50)
        self.points = []
        self.x = 0
        self.y = 0
        self.update()

    def RedrawClicked(self, e):
        self.Nimg = numpy.array(self.img)
        self.points = []
        self.y=0
        self.update()

    def BlurClicked(self):
        size, ok = QtGui.QInputDialog.getInteger(self, 'Blur Dialog',
            'size:',10, 0, 100, 1)

        if ok:
            self.Nimg=blur_(self.Nimg,size)
            self.points = []
            self.y=0
            self.update()

    def SharpenClicked(self):
        size, ok = QtGui.QInputDialog.getInteger(self, 'Sharpen Dialog',
            'size:',1, 0, 10, 1)

        if ok:
            self.Nimg=sharpen_(self.Nimg,size)
            self.points = []
            self.y=0
            self.update()

    def InvertClicked(self):
        self.Nimg=invert_(self.Nimg)
        self.points = []
        self.y=0
        self.update()

    def RotateClicked(self):
        angle, ok = QtGui.QInputDialog.getInteger(self, 'Rotate Dialog',
            'angle:',180, 0, 360, 1)

        if ok:
            self.Nimg=rotate_(self.Nimg,angle)
            self.points = []
            self.y=0
            self.update()

    def BrightClicked(self):
        bright, ok = QtGui.QInputDialog.getDouble(self, 'Brigh Dialog',
            'bright:',1.2, 0, 10, 2)

        if ok:
            self.Nimg=CC_(self.Nimg,bright,1)
            self.points = []
            self.y=0
            self.update()

    def ContrastClicked(self):
        contrast, ok = QtGui.QInputDialog.getDouble(self, 'Contrast Dialog',
            'contrast:',1.2, 0, 10, 2)

        if ok:
            self.Nimg=CC_(self.Nimg,1,contrast)
            self.points = []
            self.y=0
            self.update()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Viewport()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
