from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Hand import Hand

class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/game.ui", self)
        layout = QHBoxLayout(self)
        
        hand = Hand() #Generates a hand (Default of 7)
        for i in hand.get_cards(): #Iterates and places cards in layout
            layout.addWidget(i) #Look at Cards.py to see drawing code