from time import sleep
import random
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Hand import Hand
from Card import *
from music import AudioPlayer

class Bot():
    #Starts the bot player with a hand of 7 and no score
    def __init__(self, game_board, number):
        super().__init__()
        self.game = game_board
        self.hand = Hand()
        self.score = 0
        self.number = number # indicates which bot it is 1, 2, or 3
        self.audioPlayer = AudioPlayer()

    #Looks for a playable card. If none are found, draw a card instead and return None
    #If we want, we can add some stradegy by having it do lowest first and basing it's chance on that
    def canPlayCard(self, color, number):
        for card in self.hand.cards:
            if card.number == "WILD" or card.number == number or card.color == color:
                return card
        return None
            
    #Adds a random card to the hand
    def drawCard(self):
        new_card = self.game.genRandomCard()
        self.hand.cards.append(new_card)
        self.audioPlayer.playSoundEffect('sound/card.mp3')
        fd_card = FaceDownCard(self.number)
        if self.number == 1:
            self.game.bot1Hand.addWidget(fd_card)
        elif self.number == 2:
            self.game.bot2Hand.addWidget(fd_card)
        elif self.number == 3:
            self.game.bot3Hand.addWidget(fd_card)

    #Updates the game_Board with the properly chosen card
    def playCard(self):
        #The chance the bot gets it right based off the card num
        top_card = self.game.top_card
        card_to_play = self.canPlayCard(top_card.color, top_card.number)
        colors = ["red", "blue", "green", "yellow"]

        if card_to_play == None:
            print(f"Bot {self.number} has no playable cards. Drawing for bot...")
            self.drawCard()
            self.game.bot_status += f"\nBot {self.number} had to draw..."
        elif card_to_play.number == "WILD":
            card_to_play.setColor(random.choice(colors))
            self.updatePlayPile(card_to_play)
            self.hand.cards.remove(card_to_play)
            self.audioPlayer.playSoundEffect('sound/card.mp3')
            self.score += 1
            if self.number == 1:
                curr_bot_hand = self.game.bot1Hand
            elif self.number == 2:
                curr_bot_hand = self.game.bot2Hand
            elif self.number == 3:
                curr_bot_hand = self.game.bot3Hand

            # remove card from correct bot hand
            item = curr_bot_hand.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    curr_bot_hand.removeWidget(widget)
            self.score += 1
            print(f"Bot {self.number} playing {card_to_play.color} {card_to_play.number}")
            self.game.bot_status += f"\nBot {self.number} played a card..."
        elif random.random() < (1 - (card_to_play.number/100)):
            self.updatePlayPile(card_to_play)
            self.hand.cards.remove(card_to_play)
            self.audioPlayer.playSoundEffect('sound/card.mp3')
            # remove card from bots hand
            if self.number == 1:
                item = self.game.bot1Hand.takeAt(0)
                if item:
                    widget = item.widget()
                    if widget:
                        self.game.bot1Hand.removeWidget(widget)
                #self.game.bot1Hand.removeWidget(card_to_play)
            elif self.number == 2:
                item = self.game.bot2Hand.takeAt(0)
                if item:
                    widget = item.widget()
                    if widget:
                        self.game.bot2Hand.removeWidget(widget)
                #self.game.bot2Hand.removeWidget(card_to_play)
            elif self.number == 3:
                item = self.game.bot3Hand.takeAt(0)
                if item:
                    widget = item.widget()
                    if widget:
                        self.game.bot3Hand.removeWidget(widget)
                #self.game.bot3Hand.removeWidget(card_to_play)
            self.score += 1
            print(f"Bot {self.number} playing {card_to_play.color} {card_to_play.number}")
            self.game.bot_status += f"\nBot {self.number} played a card..."
        else:
            print(f"Bot {self.number} did not get it right")
            self.game.bot_status += f"\nBot {self.number} got the answer wrong..."
    
    #Copied the update function and changed slightly to work with bots
    def updatePlayPile(self, card_to_play):
        print(f"Bot {self.number} is playing a card...")
        print(f"Bot {self.number} Length of hand: {len(self.hand.cards)}")
        # remove top card from playPile
        self.game.playPile.removeWidget(self.game.top_card)
        # add card to top of playPile
        self.game.top_card = Card(card_to_play.color, card_to_play.number)
        self.game.top_card.question = card_to_play.question
        self.game.playPile.addWidget(self.game.top_card)

    