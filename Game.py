from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Hand import Hand

class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/game.ui", self)

        self.mainMenuButton.clicked.connect(self.clearLayout) # this is to clear the Hand layout when leaving the game screen so it can be reset
    
    """ For future reference:
        if you want to call a function with parameters on a QPushButton click,
        use lambda: self.myFunction(param1, param2, ...) when calling
        .clicked.connect() on a QPushButton
        i.e. button.clicked.connect(lambda: self.myFunction(p1, p2, p3))
        (thank you chatgpt...)
    """

    def startGame(self):
        self.layout = QHBoxLayout(self)
        hand = Hand() #Generates a hand (Default of 7)
        for i in hand.get_cards(): #Iterates and places cards in layout
            self.layout.addWidget(i) #Look at Cards.py to see drawing code
    
    # this is to clear the QHBoxLayout and its Card widgets so that when player plays again, the hand and cards are reset
    def clearLayout(self):
        while self.layout.count():
            print("removing widget")
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.layout.deleteLater()
        self.layout = None
        print("removing layout")