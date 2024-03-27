from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Hand import Hand
from Card import Card
import random
from copy import deepcopy
from Bot import Bot

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
        for i in self.hand.getCards(): #Iterates and places cards in layout
            self.handLayout.addWidget(i) #Look at Cards.py to see drawing code

        self.top_card = self.genRandomCard()
        self.playPile.addWidget(self.top_card)

        for card in self.hand.getCards():
            card.clicked.connect(self.playCard)
            card.answered_correctly.connect(self.updatePlayPileAndHand) # retrieve signal to indicate question was answered correctly
        
        num_bots, ok = QInputDialog.getInt(self, "Number of Bots", "Enter the number of bots (maximum 3):", 0, 0, 3)
        if ok:
            self.addBots(num_bots)
    
    def addCardToHand(self):
        card = self.genRandomCard()
        card.in_hand = True
        card.clicked.connect(self.playCard)
        card.answered_correctly.connect(self.updatePlayPileAndHand) # retrieve signal to indicate question was answered correctly
        self.hand.cards.append(card)
        self.handLayout.addWidget(card)
        print(self.hand.getCards())
        print(f"Adding {card.color} {card.number} to hand...")
        self.moveBots()

    def genRandomCard(self):
        colors = ['red', 'blue', 'green', 'yellow']
        random_number = random.randint(0, 9)
        random_color = random.choice(colors)
        return Card(random_color, random_number)
    
    def playCard(self, card):
        print(self.hand.cards)
        print(card)
        item = self.playPile.itemAt(0)
        top_card = item.widget()
        print("Top card is", top_card.color, top_card.number)
        print("Card clicked is", card.color, card.number)
        if (card.color == top_card.color) or (card.number == top_card.number):
            print("Card is playable")
            card.is_playable = True
        else:
            card.is_playable = False

    def updatePlayPileAndHand(self, card_to_play):
        print("updating play pile")
        print(f"Length of hand: {len(self.hand.cards)}")
        # remove top card from playPile
        self.playPile.removeWidget(self.top_card)
        # add card to top of playPile
        self.top_card = Card(card_to_play.color, card_to_play.number)
        self.top_card.question = card_to_play.question
        self.playPile.addWidget(self.top_card)
        print(f"A {card_to_play.color} {card_to_play.number} was played.")
        # remove card from hand
        print(f"Removing {card_to_play.color} {card_to_play.number} from hand")
        self.handLayout.removeWidget(card_to_play)
        self.hand.cards.remove(card_to_play)
        self.moveBots()

    
    def gameOver(self):
        dialog = QDialog()
        dialog.setWindowTitle("Game Over")

        layout = QVBoxLayout()

        label = QLabel("Game is over. Return to main menu.")
        layout.addWidget(label)

        button = QPushButton("Return to main menu.")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.setModal(True)
        dialog.exec()
        
        self.mainMenuButton.click()

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

    #Adds in the de4sired amount of bots (max 3)
    def addBots(self, num_bots):
        self.bots = []
        for i in range(num_bots):
            self.bots.append(Bot(self))

    #Makes all the bots play a valid card, if not, they draw
    def moveBots(self):
        for bot in self.bots:
            bot.playCard()