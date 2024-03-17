from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Hand import Hand
from Card import Card
import random
from copy import deepcopy

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

        self.top_card = self.genRandomCard()
        self.playPile.addWidget(self.top_card)

        for card in self.hand.get_cards():
            card.clicked.connect(self.playCard)
    
    def addCardToHand(self):
        card = self.genRandomCard()
        card.in_hand = True
        card.clicked.connect(self.playCard)
        self.hand.cards.append(card)
        self.handLayout.addWidget(card)
        print(self.hand.get_cards())
        print(f"Adding {card.color} {card.number} to hand...")

    def genRandomCard(self):
        colors = ['red', 'blue', 'green', 'yellow']
        random_number = random.randint(0, 9)
        random_color = random.choice(colors)
        return Card(random_color, random_number)
    
    def playCard(self, card):
        item = self.playPile.itemAt(0)
        top_card = item.widget()
        print("Top card is", top_card.color, top_card.number)
        print("Card clicked is", card.color, card.number)
        if (card.color == top_card.color) or (card.number == top_card.number):
            print("Card is playable")
            card.is_playable = True
            card.answered_correctly.connect(lambda: self.updatePlayPile(card)) # retrieve signal to indicate question was answered correctly

    def updatePlayPile(self, card_to_play):
        # remove top card from playPile
        self.playPile.removeWidget(self.top_card)
        # add card to top of playPile
        self.top_card = Card(card_to_play.color, card_to_play.number)
        self.top_card.question = card_to_play.question
        self.playPile.addWidget(self.top_card)
        print(f"A {card_to_play.color} {card_to_play.number} was played.")

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