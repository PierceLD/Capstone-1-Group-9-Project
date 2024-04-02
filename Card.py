from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from random import choice
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
    dialog_closed = pyqtSignal()
    def hideCard(self, correct):
        if correct:
            print("correct, hiding card")
            self.answered_correctly.emit(self) # send the signal that answer has been correctly answered
            self.question_popup.dialog_closed.connect(lambda: self.dialog_closed.emit()) # send signal that "correct/incorrect" dialog has been closed
            self.hide()
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
    wild_delete = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit(self)
        if event.button() == Qt.MouseButton.LeftButton:
            if self.in_hand and self.is_playable:
                self.wild_delete.connect(self.hideWildCard)
                self.answered_correctly.emit(self)
                self.wild_delete.emit()
                self.dialog_closed.emit()
                print(f"clicked a card {self.color} {self.number}") # this is for debugging purposes
    
    def hideWildCard(self):
        self.hide()
        self.deleteLater()

    def setColor(self, color):
        self.color = color
        self.update()

class DrawCard(Card):
    def __init__(self, color):
        super().__init__(color, "DRAW")
        self.power = choice([2,4])
        self.symbol = "+" + str(self.power)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.fillRect(self.rect(), QColor(self.color))
        painter.setPen(QColor("black")) if self.color == "yellow" or self.color == "red" else painter.setPen(QColor("white"))
        pixmap = QPixmap("./img/card.png")
        painter.drawPixmap(0, 0, 100, 152, pixmap)
        painter.drawText(QPoint(15, 30), self.symbol)
        painter.drawText(QPoint(75, 132), self.symbol)
        
    clicked = pyqtSignal(QWidget)
    draw_delete = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit(self)
        if event.button() == Qt.MouseButton.LeftButton:
            if self.in_hand and self.is_playable:
                self.draw_delete.connect(self.hideDrawCard)
                self.answered_correctly.emit(self)
                self.draw_delete.emit()
                self.dialog_closed.emit()
                print(f"clicked a card {self.color} {self.number}")
    
    def hideDrawCard(self):
        self.hide()
        self.deleteLater()