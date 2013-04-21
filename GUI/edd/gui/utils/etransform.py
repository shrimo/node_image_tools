import math
from PyQt4.QtCore import QPointF

class ETransform:
    def __init__(self):
        return
    
    @staticmethod
    def rotatePoint( radius, angle):
        return QPointF( math.sin(math.radians( angle ))* radius + math.cos(math.radians( angle ))* 0.0,
                        math.cos(math.radians( angle ))* radius - math.sin(math.radians( angle ))* 0.0)      
        