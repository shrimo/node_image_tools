import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class EDraw():
    
    class EColor():

        DefaultFillColor = QColor(35, 36, 37)

        DefaultAttributeFillColor = QColor(60, 63, 65)

        DefaultTitleColor = QColor(43, 43, 43)
        DefaultTitleTextColor = Qt.darkGray

        DefaultNodeFillColor = Qt.darkGray

        DefaultSelectionColor = QColor(247, 147, 30)
        DefaultEnterHoverPen = QPen(QColor(247, 147, 30), 1, Qt.SolidLine)
        DefaultLeaveHoverPen = QPen(QColor(61,62,65), 1 , Qt.SolidLine)
        
        def __init__(self):
            return
        
        @staticmethod
        def LinearGradient(nodeRect, nodeColor = Qt.gray ):
            g = QLinearGradient(0, -nodeRect.height(), 0, nodeRect.height())
            g.setColorAt(0, Qt.black)
            g.setColorAt(0.3, nodeColor )
            g.setColorAt(1, Qt.black )
            return g

        @staticmethod
        def NodeRadialGradient( center = QPointF(0.0, 0.0), radius = 1.0, color = Qt.gray):
            g = QRadialGradient( center.x(), center.y() , radius)
            g.setColorAt(0, color)
            g.setColorAt(1, EDraw.EColor.DefaultFillColor)
            return g   
    
    def __init__(self):        
        return

    @staticmethod
    def DefaultPolygon( width, height ):
        browserNode = QPolygonF( QRectF( 0.0, 0.0 , width - height, height  ))

        c1 = EDraw.Circle( height/2, 24).translated( 0.0, height/2)

        browserNode = browserNode.united(c1)

        c2 = EDraw.Circle(height/2, 24).translated( width - height, height/2 )

        return browserNode.united(c2).translated( height/2, 0.0 )
    
    @staticmethod
    def Circle(radius, pointNum, startAngle = 0.0 ):
        cPolygon = QPolygonF()
        cPolygon.clear()               
        
        step = (math.pi*2) / pointNum 
        cStep = math.radians(startAngle)
        for i in range(0,pointNum):
            x2 = math.cos(cStep)*radius - math.sin(cStep)*0.0
            y2 = math.sin(cStep)*radius + math.cos(cStep)*0.0
            cPolygon.append(QPointF(x2,y2))
            cStep += step       
                      
        return cPolygon
    
    @staticmethod
    def Pie( startAngle, endAngle, step, radius1, radius2, pointNum, offset):
        cPolygon = QPolygonF()
        cPolygon.clear()
        cPolygon.append(QPointF(0,0))               
        
        iStep = ((math.pi*2)/step) / pointNum
        startStep = math.radians(startAngle)
        endStep = math.radians(endAngle)
               
        for i in range(0,pointNum+1):
            x2 = math.cos(startStep)*radius1 - math.sin(startStep)
            y2 = math.sin(startStep)*radius1 + math.cos(startStep)          
            cPolygon.append(QPointF(x2,y2))
            startStep += iStep
                      
        return cPolygon.subtracted(EDraw.Circle(radius2, pointNum))
       
    @staticmethod
    def ring(outRadius, inRadius, pointNum):
        cPolygon = EDraw.Circle(outRadius, pointNum)
        return cPolygon.subtracted(EDraw.Circle(inRadius, pointNum))

    @staticmethod
    def resourceHandle():
        p1 = EDraw.Pie(180-45, 180+45, 4, 35, 0, 24, 0 )
        p2 = EDraw.Circle(30, 50).united( EDraw.Pie( 360-45, 45, 4, 35, 0, 24, 0 ) )
        return p1.united(p2)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        