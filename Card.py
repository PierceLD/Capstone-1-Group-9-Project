from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Question_Popup import Question_Popup
from Question import Question

#Class for the movable You-Know Cards
class Card(QWidget): 
    def __init__(self, color, number):
        super().__init__()
        self.color = color
        self.number = number
        self.question = Question(self.color).question
        self.setFixedSize(100, 152)
        self.setMouseTracking(True)
        self.is_playable = False
        self.in_hand = False
        
    #Function for painting You-Know Cards (Works real time)   
    def paintEvent(self, event): 
        painter = QPainter(self)
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor("black")) if self.color == "yellow" or self.color == "red" else painter.setPen(QColor("white"))
        #Set 100x150 px to random color and random number in corner
        painter.fillRect(self.rect(), QColor(self.color))
        painter.drawText(QPoint(15, 30), str(self.number))
        painter.drawText(QPoint(75, 132), str(self.number))

        pixmap = QPixmap("./img/card.png")
        painter.drawPixmap(0, 0, 100, 152, pixmap)

        pen = QPen(QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(self.rect())
    
    #Event when mouse is pressed
    clicked = pyqtSignal(QWidget)
    def mousePressEvent(self, event):
        self.clicked.emit(self)
        if event.button() == Qt.MouseButton.LeftButton:
            if self.in_hand and self.is_playable:
                self.question_popup = Question_Popup(self.question)
                self.question_popup.playerAns.connect(self.hideCard)
                self.question_popup.show_popup()
                print(f"clicked a card {self.color} {self.number}") # this is for debugging purposes

    answered_correctly = pyqtSignal(QWidget)
    def hideCard(self, correct):
        if correct:
            self.answered_correctly.emit(self) # send the signal that answer has been correctly answered
            self.deleteLater()
        else:
            print("incorrect")

class WildCard(Card):
    def __init__(self, color):
        super().__init__("WILD", "WILD")

    def paintEvent(self, event): 
        painter = QPainter(self)
        font = painter.font()
        font.setPointSize(15)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor("black")) if self.color == "yellow" or self.color == "red" else painter.setPen(QColor("white"))
        #Set 100x150 px to random color and random number in corner
        if self.color == "WILD":
            painter.fillRect(self.rect(), QColor("Black"))
        else:
            painter.fillRect(self.rect(), QColor(self.color))
        pixmap = QPixmap("./img/card.png")
        painter.drawPixmap(0, 0, 100, 152, pixmap)

        if self.color == "WILD":
            pen = QPen(QColor("black"))
        else:
            pen = QPen(QColor(self.color))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(self.rect())

        colors = ["red", "blue", "green", "yellow"]
        letters = ['W', 'I', 'L', 'D']
        letter_spacing = 18
        if self.color == "WILD":
            for i in range(len(colors)):
                painter.setPen(QColor(colors[i]))
                painter.drawText(20 + i * letter_spacing, 110 - i * letter_spacing, letters[i])
        else:
            for i in range(len(colors)):
                painter.setPen(QColor("Black"))
                painter.drawText(20 + i * letter_spacing, 110 - i * letter_spacing, letters[i])

     #Event when mouse is pressed
    clicked = pyqtSignal(QWidget)
    def mousePressEvent(self, event):
        self.clicked.emit(self)
        if event.button() == Qt.MouseButton.LeftButton:
            if self.in_hand and self.is_playable:
                self.answered_correctly.emit(self)
                print(f"clicked a card {self.color} {self.number}") # this is for debugging purposes

    def setColor(self, color):
        self.color = color
        self.update()