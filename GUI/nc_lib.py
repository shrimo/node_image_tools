import sys
from PyQt4.QtCore import Qt, QByteArray
from PyQt4.QtGui import QApplication, QMainWindow, QSplitter, QTabWidget, QTextEdit, QLabel, QImage, QPixmap

from edd.gui.escene import EScene
from edd.gui.eview import EView

from edd.core.enodehandle import ENodeHandle

from PIL import Image, ImageQt, ImageChops
from scipy import misc
import numpy

class ViewNode(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)

        self.IsStatic = True

        self.__inputAttr = self.addInputAttribute("Input")

        self.__control = None

    def setControl(self, control):
        self.__control = control

    def compute(self):

        img32bit= self.__inputAttr.Data
        img8bit = img32bit.astype('uint8')
        im = Image.fromarray(img8bit)
        RGBdata = None or im.convert("RGBA").tostring("raw", "BGRA")

        image = QImage(RGBdata, im.size[0], im.size[1], QImage.Format_ARGB32)
        pix = QPixmap.fromImage(image)

        self.__control.setPixmap(pix)

        print "%s Computed" % self.Name

class WriteNode(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)

        self.IsStatic = True

        self.__inputAttr = self.addInputAttribute("Input")

        self.__control = None

    def setControl(self, control):
        self.__control = control

    def compute(self):
        
        self.__inputAttr.Data.astype('uint8')
        im = Image.fromarray(self.__inputAttr.Data)
        im.save('out.jpg')

        print "%s Computed" % self.Name

class ReadNode(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)

        self.__inputAttr = Image.open("crop.jpg")
        self.__outputAttr = self.addOutputAttribute("Output")

    def compute(self):
        imageFloat = numpy.array(self.__inputAttr)
        imageFloat = imageFloat.astype(float)
        self.__outputAttr.Data = imageFloat
        
        print "%s Computed..." % self.Name

class ReadNode2(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)

        self.__inputAttr = Image.open("merge.jpg")
        self.__outputAttr = self.addOutputAttribute("Output")

    def compute(self):
        imageFloat = numpy.array(self.__inputAttr)
        imageFloat = imageFloat.astype(float)
        self.__outputAttr.Data = imageFloat

        print "%s Computed..." % self.Name


class BlurNode(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)

        #self.__size = 5
        self.__size = self.addProperty("Size", 10)
        self.__inputAttr = self.addInputAttribute("Input")
        self.__outputAttr = self.addOutputAttribute("Output")

    def compute(self):

        if self.__inputAttr.Data is None:
            return

        from scipy import ndimage
        theData = self.__inputAttr.Data

        r = theData[:, :, 0]
        g = theData[:, :, 1]
        b = theData[:, :, 2]
        
        r = ndimage.gaussian_filter(r, order=0, sigma=self.__size.Data)
        g = ndimage.gaussian_filter(g, order=0, sigma=self.__size.Data)
        b = ndimage.gaussian_filter(b, order=0, sigma=self.__size.Data)

        self.__outputAttr.Data = numpy.dstack((r, g, b))

        print "%s Computed" % self.Name

class SizeNode(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)
        self.__size = 1.2
        self.__inputAttr = self.addInputAttribute("Input")
        self.__outputAttr = self.addOutputAttribute("Output")

    def compute(self):

        if self.__inputAttr.Data is None:
            return
        img = Image.fromarray(self.__inputAttr.Data)
        w, h = img.size
        if (self.__size>0):
            S= int(round(h*self.__size)), int(round(w*self.__size))
            self.__outputAttr.Data=misc.imresize(self.__inputAttr.Data,S,'bilinear','RGB')
        if (self.__size<0):
            S= int(round(h/abs(self.__size))),int(round(w/abs(self.__size)))
            self.__outputAttr.Data=misc.imresize(self.__inputAttr.Data,S,'bilinear','RGB')

        print "%s Computed" % self.Name

class CompositeNode(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)
        self.__inputAttrA = self.addInputAttribute("InputA")
        self.__inputAttrB = self.addInputAttribute("InputB")
        self.__outputAttr = self.addOutputAttribute("Output")

    def compute(self):
        self.__outputAttr.Data=self.__inputAttrA.Data + self.__inputAttrB.Data

class ColorSpaceNode(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)
        self.__inputAttrA = self.addInputAttribute("InputA")
        self.__outputAttr = self.addOutputAttribute("Output")

    def compute(self):
        display_min = 0
        display_max = 255
        image_data = self.__inputAttrA.Data
        threshold_image = ((image_data.astype(float) - display_min) *
                           (image_data > display_min))
        scaled_image = (threshold_image * (255. / (display_max - display_min)))
        scaled_image[scaled_image > 255] = 255
        self.__outputAttr.Data=scaled_image.astype(numpy.uint8)

        


                                    
