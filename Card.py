from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

#Class for the movable You-Know Cards
class Card(QWidget): 
    def __init__(self, color, number):
        super().__init__()
        self.color = color
        self.number = number
        self.setFixedSize(100, 150)
        self.setMouseTracking(True)
        self.offset = 0 #Offset for going to event pos
        
    #Function for painting You-Know Cards (Works real time)   
    def paintEvent(self, event): 
        painter = QPainter(self)
        font = painter.font()
        font.setPointSize(12)
        painter.setFont(font)
        #Set 100x150 px to random color and random number in corner
        painter.fillRect(self.rect(), QColor(self.color))
        painter.drawText(QPoint(5, 15), str(self.number))
    
    #Event when mouse is pressed to get the offset
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.offset = event.pos()
            
    #As long as LMB is pushed, the card will folllow the mouse within the layout
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            new_pos = self.mapToParent(event.pos() - self.offset)
            self.move(new_pos)