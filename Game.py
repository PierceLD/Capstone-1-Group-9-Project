from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Hand import Hand
from Card import *
import random
from copy import deepcopy
from Bot import Bot
from music import AudioPlayer
from Database import *

class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/game.ui", self)
        self.audioPlayer = AudioPlayer()

        # default random set-color mappings
        self.set_names = getAllSetNames()
        self.all_set_names = self.set_names[:]
        self.red_set = random.choice(self.all_set_names)
        self.all_set_names.remove(self.red_set)
        self.blue_set = random.choice(self.all_set_names)
        self.all_set_names.remove(self.blue_set)
        self.green_set = random.choice(self.all_set_names)
        self.all_set_names.remove(self.green_set)
        self.yellow_set = random.choice(self.all_set_names)

        self.mainMenuButton.clicked.connect(self.resetLayout) # this is to clear the Hand layout when leaving the game screen so it can be reset
        self.drawButton.clicked.connect(self.drawCard)

        self.bots_finished.connect(self.enableScreen)

        self.current_player = "You"

        self.game_over = False

    def startGame(self):
        # handles if a set is deleted, needs to be at least 1 set present at all times.
        self.set_names = getAllSetNames()
        if self.red_set not in self.set_names:
            self.red_set = random.choice(self.set_names)
        if self.blue_set not in self.set_names:
            self.blue_set = random.choice(self.set_names)
        if self.green_set not in self.set_names:
            self.green_set = random.choice(self.set_names)
        if self.yellow_set not in self.set_names:
            self.yellow_set = random.choice(self.set_names)
        print(f"Red is set {self.red_set}")
        print(f"Blue is set {self.blue_set}")
        print(f"Green is set {self.green_set}")
        print(f"Yellow is set {self.yellow_set}")

        self.hand = Hand(self) #Generates a hand (Default of 7)
        self.bots = []
        self.game_over = False

        self.player_status = "It's your turn."
        self.statusLabel.setText(self.player_status)

        for i in self.hand.getCards(): #Iterates and places cards in layout
            self.handLayout.addWidget(i) #Look at Cards.py to see drawing code

        self.top_card = self.genRandomCard()
        #If the top card is a wild card, give it a random color
        if self.top_card.color == "WILD":
            self.top_card.setColor(random.choice(["red", "blue", "green", "yellow"]))
        self.playPile.addWidget(self.top_card)

        for card in self.hand.getCards():
            card.clicked.connect(self.playCard)
            card.answered_correctly.connect(self.updatePlayPileAndHand) # retrieve signal to indicate question was answered correctly
            card.dialog_closed.connect(self.checkGameOver) # check if player won, then move bots if not
            card.dialog_closed.connect(self.moveBots) # forced user to close correct/incorrect dialog for bots to start playing
        
        num_bots, ok = QInputDialog.getInt(self, "Number of Bots", "Enter the number of bots (maximum 3):", 0, 0, 3)
        if ok:
            self.addBots(num_bots)
        else:
            num_bots = 0
            self.addBots(num_bots)
        
        for i, bot in enumerate(self.bots):
            if i == 0:
                for card in bot.hand.getCards(): #Iterates and places cards in layout
                    fd_card = FaceDownCard(bot.number)
                    self.bot1Hand.addWidget(fd_card) #Look at Cards.py to see drawing code
            elif i == 1:
                for card in bot.hand.getCards(): #Iterates and places cards in layout
                    fd_card = FaceDownCard(bot.number)
                    self.bot2Hand.addWidget(fd_card) #Look at Cards.py to see drawing code
            elif i == 2:
                for card in bot.hand.getCards(): #Iterates and places cards in layout
                    fd_card = FaceDownCard(bot.number)
                    self.bot3Hand.addWidget(fd_card) #Look at Cards.py to see drawing code

    def drawCard(self):
        if self.current_player == "You":
            self.audioPlayer.playSoundEffect('sound/card.mp3')
            card = self.genRandomCard()
            card.in_hand = True
            card.clicked.connect(self.playCard)
            card.answered_correctly.connect(self.updatePlayPileAndHand) # retrieve signal to indicate question was answered correctly
            card.dialog_closed.connect(self.checkGameOver) # check if player won, then move bots if not
            card.dialog_closed.connect(self.moveBots) # forced user to close correct/incorrect dialog for bots to start playing
            self.hand.cards.append(card)
            self.handLayout.addWidget(card)
            print(self.hand.getCards())
            print(f"Adding {card.color} {card.number} to hand...")
            # end players turn and move on to bots
            self.moveBots()

    def genRandomCard(self):
        colors = ['red', 'blue', 'green', 'yellow']
        random_number = random.randint(-1, 9)
        if random_number == -1:  
            return WildCard(self)
        else:
            random_color = random.choice(colors)
            return Card(random_color, random.randint(0, 9), self)
    
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


    def updatePlayPileAndHand(self, card_to_play, correct):
        if correct:
            player_correct_msg = self.player_status + "\nYou got to play!"
            self.statusLabel.setText(player_correct_msg)
            print("updating play pile")
            print(f"Length of hand: {len(self.hand.cards)}")
            # remove top card from playPile
            self.playPile.removeWidget(self.top_card)
            # add card to top of playPile
            if card_to_play.number == "WILD":
                self.top_card = WildCard(self)
                self.top_card.setColor(card_to_play.color)
            else:
                self.top_card = Card(card_to_play.color, card_to_play.number, self)
                self.top_card.question = card_to_play.question
            self.playPile.addWidget(self.top_card)
            print(f"A {card_to_play.color} {card_to_play.number} was played.")
            # remove card from hand
            print(f"Removing {card_to_play.color} {card_to_play.number} from hand")
            self.handLayout.removeWidget(card_to_play)
            self.hand.cards.remove(card_to_play)
            self.audioPlayer.playSoundEffect('sound/card.mp3')
        else: # player answered incorrectly, skip to bots turns
            player_incorrect_msg = self.player_status + "\nLose your turn..."
            self.statusLabel.setText(player_incorrect_msg)

    def checkGameOver(self):
        print("Checking if game is over.")
        if len(self.hand.cards) == 0:
            msg = "You Win!"
            self.audioPlayer.playSoundEffect('sound/win.mp3')
            self.game_over = True
            self.enableScreen()
            self.gameOver(msg)
        else:
            for bot in self.bots:
                if (len(bot.hand.cards) == 0) and (not self.game_over):
                    self.game_over = True
                    self.bots_finished.emit()
                    msg = f"Bot {bot.number} Wins!"
                    self.audioPlayer.playSoundEffect('sound/lose.mp3')
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

    #Adds in the de4sired amount of bots (max 3)
    def addBots(self, num_bots):
        for i in range(num_bots):
            self.bots.append(Bot(self, i+1))

    #Makes all the bots play a valid card, if not, they draw
    bots_finished = pyqtSignal()
    def moveBots(self):
        if len(self.bots) > 0 and not self.game_over:
            print("Bots playing...")
            self.disableScreen() # disable everything user can click on screen so user can't interact while bots are playing
            print("Executing delay")
            self.executeDelay(750)
            print("Delay finished")

            for bot in self.bots:
                self.current_player = f"Bot {bot.number}"
                self.bot_status = f"It's Bot {bot.number}'s turn."
                self.statusLabel.setText(self.bot_status)
                bot.playCard()
                self.statusLabel.setText(self.bot_status)
                self.checkGameOver()
                if not self.game_over:
                    print("Executing delay")
                    self.executeDelay(1250)
                    print("Delay finished")
                else:
                    print(f"Game over. Bot {bot.number} wins!")
                    break
            
            self.bots_finished.emit() # signal that bots are finished playing this round to enable screen again
            self.current_player = "You"
            self.statusLabel.setText("It's your turn.")

    def disableScreen(self):
        print("screen disabled")
        # manually disable each clickable widget, except for mute button
        for i in range(self.handLayout.count()):
            item = self.handLayout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setDisabled(True)
        self.mainMenuButton.setDisabled(True)
        self.setStyleSheet("""QPushButton { color: black; }""") # prevent button text from greying out

    def enableScreen(self):
        print("screen reenabled")
        # reenable each clickable widget
        for i in range(self.handLayout.count()):
            item = self.handLayout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setEnabled(True)
        self.mainMenuButton.setEnabled(True)

    def executeDelay(self, time_in_ms):
        loop = QEventLoop()
        QTimer.singleShot(time_in_ms, loop.quit)
        loop.exec()

    # this is to clear the QHBoxLayout and its Card widgets so that when player plays again, the hand and cards are reset
    def resetLayout(self):
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