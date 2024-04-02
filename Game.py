from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Hand import Hand
from Card import Card
from Card import WildCard
import random
from copy import deepcopy
from Bot import Bot
from music import AudioPlayer

class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/game.ui", self)
        self.audioPlayer = AudioPlayer()

        self.mainMenuButton.clicked.connect(self.clearLayout) # this is to clear the Hand layout when leaving the game screen so it can be reset
        self.drawButton.clicked.connect(self.addCardToHand)

        self.bot_finished.connect(self.enableScreen)

    def startGame(self):
        self.hand = Hand() #Generates a hand (Default of 7)
        for i in self.hand.getCards(): #Iterates and places cards in layout
            self.handLayout.addWidget(i) #Look at Cards.py to see drawing code

        #self.top_card = self.genRandomCard()
        self.top_card = WildCard("WILD")
        #If the top card is a wild card, give it a random color
        if self.top_card.color == "WILD":
            self.top_card.setColor(random.choice(["red", "blue", "green", "yellow"]))
        self.playPile.addWidget(self.top_card)

        for card in self.hand.getCards():
            card.clicked.connect(self.playCard)
            card.answered_correctly.connect(self.updatePlayPileAndHand) # retrieve signal to indicate question was answered correctly
        
        num_bots, ok = QInputDialog.getInt(self, "Number of Bots", "Enter the number of bots (maximum 3):", 0, 0, 3)
        if ok:
            self.addBots(num_bots)
        else:
            num_bots = 0
            self.addBots(num_bots)
        
        for i, bot in enumerate(self.bots):
            if i == 0:
                for card in bot.hand.getCards(): #Iterates and places cards in layout
                    self.bot1Hand.addWidget(card) #Look at Cards.py to see drawing code
            elif i == 1:
                for card in bot.hand.getCards(): #Iterates and places cards in layout
                    self.bot2Hand.addWidget(card) #Look at Cards.py to see drawing code
            elif i == 2:
                for card in bot.hand.getCards(): #Iterates and places cards in layout
                    self.bot3Hand.addWidget(card) #Look at Cards.py to see drawing code

    def addCardToHand(self):
        self.audioPlayer.playSoundEffect('sound/card.mp3')
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
        random_number = random.randint(-1, 9)
        if random_number == -1:  
            return WildCard(random.choice(colors))
        else:
            random_color = random.choice(colors)
            return Card(random_color, random.randint(0, 9))
    
    def playCard(self, card):
        print(self.hand.cards)
        print(card)
        item = self.playPile.itemAt(0)
        top_card = item.widget()
        print("Top card is", top_card.color, top_card.number)
        print("Card clicked is", card.color, card.number)
        if card.color == "WILD":
            choices = ["red", "blue", "green", "yellow"]
            item, ok = QInputDialog.getItem(self, "Select an option", "Options:", choices, editable=False)
            if ok:
                print("Selected option:", item)
                card.setColor(item)
                card.is_playable = True
        elif (card.color == top_card.color) or (card.number == top_card.number):
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
        if card_to_play.number == "WILD":
            self.top_card = WildCard("WILD")
            self.top_card.setColor(card_to_play.color)
        else:
            self.top_card = Card(card_to_play.color, card_to_play.number)
            self.top_card.question = card_to_play.question
        self.playPile.addWidget(self.top_card)
        print(f"A {card_to_play.color} {card_to_play.number} was played.")
        # remove card from hand
        print(f"Removing {card_to_play.color} {card_to_play.number} from hand")
        self.handLayout.removeWidget(card_to_play)
        self.hand.cards.remove(card_to_play)
        self.audioPlayer.playSoundEffect('sound/card.mp3')
        card_to_play.dialog_closed.connect(self.checkGameOver)
        if len(self.hand.cards) > 0:
            card_to_play.dialog_closed.connect(self.moveBots) # forced user to close correct/incorrect dialog for bots to start playing

    def checkGameOver(self):
        print("Checking if game is over.")
        if len(self.hand.cards) == 0:
            msg = "You Win!"
            self.gameOver(msg)
        else:
            for bot in self.bots:
                if len(bot.hand.cards) == 0:
                    msg = f"Bot {bot.number} Wins!"
                    self.gameOver(msg)
                    break

    def gameOver(self, msg):
        dialog = QDialog()
        dialog.setWindowTitle("Game Over")

        layout = QVBoxLayout()

        label = QLabel(msg)
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

        while self.bot1Hand.count():
            print("removing widget")
            item = self.bot1Hand.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        while self.bot2Hand.count():
            print("removing widget")
            item = self.bot2Hand.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        while self.bot3Hand.count():
            print("removing widget")
            item = self.bot3Hand.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    #Adds in the de4sired amount of bots (max 3)
    def addBots(self, num_bots):
        self.bots = []
        for i in range(num_bots):
            self.bots.append(Bot(self, i+1))

    #Makes all the bots play a valid card, if not, they draw
    bot_finished = pyqtSignal()
    def moveBots(self):
        self.setDisabled(True) # disable everything on screen so user can't click when bots are playing
        # TODO: fix background greying out
        self.setStyleSheet("""
            QPushButton {
                color: black;
            }
            QLabel {
                color: black;
            }
        """)
        self.num_shots = len(self.bots)
        if len(self.bots) >= 1:
            QTimer.singleShot(1500, lambda: self.botToPlay(self.bots[0]))
            
        if len(self.bots) >= 2:
            QTimer.singleShot(2*1500, lambda: self.botToPlay(self.bots[1]))
            
        if len(self.bots) == 3:
            QTimer.singleShot(3*1500, lambda: self.botToPlay(self.bots[2]))
            

    def botToPlay(self, bot):
        bot.playCard()
        self.checkGameOver()
        self.num_shots -= 1
        self.bot_finished.emit()

    def enableScreen(self):
        if self.num_shots == 0:
            print("screen reenabled")
            self.setEnabled(True)