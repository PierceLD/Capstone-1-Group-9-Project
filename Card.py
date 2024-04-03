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
        if self.number != "WILD":
            painter.drawText(QPoint(15, 30), str(self.number))
            painter.drawText(QPoint(75, 132), str(self.number))
            pixmap = QPixmap("./img/card.png")
        else:
            pixmap = QPixmap("./img/wild.png")
            painter.fillRect(self.rect(), QColor(self.color))
            
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

    answered_correctly = pyqtSignal(QWidget, bool)
    answered_incorrectly = pyqtSignal()
    dialog_closed = pyqtSignal()
    def hideCard(self, correct):
        if correct:
            print("correct, hiding card")
            self.answered_correctly.emit(self, True) # send the signal that question has been correctly answered
            self.question_popup.dialog_closed.connect(lambda: self.dialog_closed.emit()) # send signal that "correct/incorrect" dialog has been closed
            self.hide()
            self.deleteLater()
        else:
            self.answered_correctly.emit(self, False) # send the signal that question has been incorrectly answered
            self.question_popup.dialog_closed.connect(lambda: self.dialog_closed.emit()) # send signal that "correct/incorrect" dialog has been closed
            print("incorrect, lose your turn")

class WildCard(Card):
    def __init__(self, color):
        super().__init__("WILD", "WILD")

    def paintEvent(self, event): 
        painter = QPainter(self)
        #Set 100x150 px to random color and random number in corner
        if self.color == "WILD":
            painter.fillRect(self.rect(), QColor("Black"))
        else:
            painter.fillRect(self.rect(), QColor(self.color))
        pixmap = QPixmap("./img/wild.png")
        painter.drawPixmap(0, 0, 100, 152, pixmap)

        colors = ["red", "blue", "green", "yellow"]
        if self.color == "WILD":
            for i in range(len(colors)):
                painter.setPen(QColor(colors[i]))
        else:
            for i in range(len(colors)):
                painter.setPen(QColor("Black"))

    #Event when mouse is pressed
    clicked = pyqtSignal(QWidget)
    delete = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit(self)
        if event.button() == Qt.MouseButton.LeftButton:
            if self.in_hand and self.is_playable:
                self.delete.connect(self.hideWildCard)
                self.answered_correctly.emit(self, True)
                self.delete.emit()
                self.dialog_closed.emit()
                print(f"clicked a card {self.color} {self.number}") # this is for debugging purposes
    
    def hideWildCard(self):
        self.hide()
        self.deleteLater()

    def setColor(self, color):
        self.color = color
        self.update()

class FaceDownCard(QWidget):
    def __init__(self, bot_num):
        super().__init__()
        self.bot_num = bot_num
        if bot_num == 1 or bot_num == 3:
            self.setFixedSize(114, 75)
        else:
            self.setFixedSize(75, 114)

    def paintEvent(self, event):
        painter = QPainter(self)

        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor("black"))
        #Set 100x150 px to random color and random number in corner
        painter.fillRect(self.rect(), QColor("transparent"))
        painter.drawText(QPoint(15, 30), "")
        painter.drawText(QPoint(75, 132), "")

        if self.bot_num == 1:
            pixmap = QPixmap("img/card_back_bot1.png")
            painter.drawPixmap(0, 0, 114, 75, pixmap)
        elif self.bot_num == 2:
            pixmap = QPixmap("img/card_back_bot2.png")
            painter.drawPixmap(0, 0, 75, 114, pixmap)
        else:
            pixmap = QPixmap("img/card_back_bot3.png")
            painter.drawPixmap(0, 0, 114, 75, pixmap)

        pen = QPen(QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(self.rect())