from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Hand import Hand
from Card import Card
import random

class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/game.ui", self)

        self.mainMenuButton.clicked.connect(self.clearLayout) # this is to clear the Hand layout when leaving the game screen so it can be reset
        self.drawButton.clicked.connect(self.addCardToHand)
    
    """ For future reference:
        if you want to call a function with parameters on a QPushButton click,
        use lambda: self.myFunction(param1, param2, ...) when calling
        .clicked.connect() on a QPushButton
        i.e. button.clicked.connect(lambda: self.myFunction(p1, p2, p3))
        (thank you chatgpt...)
    """

    def startGame(self):
        self.hand = Hand() #Generates a hand (Default of 7)
        for i in self.hand.get_cards(): #Iterates and places cards in layout
            self.handLayout.addWidget(i) #Look at Cards.py to see drawing code

        self.top_card = self.genRandomCard(0)
        self.playPile.addWidget(self.top_card)

        for card in self.hand.get_cards():
            card.clicked.connect(self.playCard)
    
    def addCardToHand(self):
        hand_length = len(self.hand.cards)
        card = self.genRandomCard(hand_length + 1)
        self.hand.cards.append(card)
        self.handLayout.addWidget(card)
        print(self.hand.get_cards())
        print(f"Adding {card.color} {card.number} to hand...")

    def genRandomCard(self, index):
        colors = ['red', 'blue', 'green', 'yellow']
        random_number = random.randint(0, 9)
        random_color = random.choice(colors)
        return Card(random_color, random_number, index)
    
    def playCard(self, color, number):
        # remove top card from playPile
        item = self.playPile.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
        # add new card to top of playPile
        self.top_card = Card(color, number, 0)
        self.playPile.addWidget(self.top_card)
        print(f"A {color} {number} was played.")

    # this is to clear the QHBoxLayout and its Card widgets so that when player plays again, the hand and cards are reset
    def clearLayout(self):
        while self.handLayout.count():
            print("removing widget")
            item = self.handLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        while self.playPile.count():
            print("removing widget")
            item = self.playPile.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()