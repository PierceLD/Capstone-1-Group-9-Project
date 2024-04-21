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
        self.hand = Hand(self.game)
        self.number = number # indicates which bot it is 1, 2, or 3
        self.audioPlayer = AudioPlayer()

    #Looks for a playable card. If none are found, draw a card instead and return None
    #If we want, we can add some stradegy by having it do lowest first and basing it's chance on that
    def canPlayCard(self, color, number):
        for card in self.hand.cards:
            if card.number == "WILD" or str(card.number) == str(number) or card.color == color:
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

        # handles skips, reverses, and draw 2's chance for bot to not play, since these cards have questions
        if card_to_play != None:
            card_num = card_to_play.number
            if str(card_num) == "Skip":
                card_num = 10
            elif str(card_num) == "Reverse":
                card_num = 11
            elif str(card_num) == "Draw 2":
                card_num = 12
            else:
                card_num = card_to_play.number

        if card_to_play == None:
            print(f"Bot {self.number} has no playable cards. Drawing for bot...")
            self.drawCard()
            self.game.bot_status = f"Bot {self.number} had to draw..."
        elif card_to_play.number == "WILD":
            card_to_play.setColor(random.choice(colors))
            self.updatePlayPile(card_to_play)
            self.hand.cards.remove(card_to_play)
            self.audioPlayer.playSoundEffect('sound/card.mp3')
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
            print(f"Bot {self.number} playing {card_to_play.color} {card_to_play.number}")
            self.game.bot_status = f"Bot {self.number} played..."

        elif card_to_play.number == "DRAW": # TODO: remove or modify
            self.updatePlayPile(card_to_play)
            self.hand.cards.remove(card_to_play)
            self.audioPlayer.playSoundEffect('sound/card.mp3')
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
            print(f"Bot {self.number} playing {card_to_play.color} {card_to_play.number}")
            self.game.bot_status = f"Bot {self.number} played..."

        elif random.random() < (1 - (card_num/100)): # also handles skips, reverses, draw 2's
            self.updatePlayPile(card_to_play)
            self.hand.cards.remove(card_to_play)
            self.audioPlayer.playSoundEffect('sound/card.mp3')
            self.removeCardFromHand()
            print(f"Bot {self.number} playing {card_to_play.color} {card_to_play.number}")
            self.game.bot_status = f"Bot {self.number} played..."
            if str(card_to_play.number) == "Skip": # used to skip next players turn
                self.game.skip_played = True
            elif str(card_to_play.number) == "Reverse":
                self.game.reverse_played = True
            elif str(card_to_play.number) == "Draw 2":
                self.game.draw_card_played = True
        else:
            print(f"Bot {self.number} did not get it right")
            self.game.bot_status = f"Bot {self.number} answered wrong..."

    def removeCardFromHand(self):
        # remove card from bots hand
        if self.number == 1:
            item = self.game.bot1Hand.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    self.game.bot1Hand.removeWidget(widget)
        elif self.number == 2:
            item = self.game.bot2Hand.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    self.game.bot2Hand.removeWidget(widget)
        elif self.number == 3:
            item = self.game.bot3Hand.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    self.game.bot3Hand.removeWidget(widget)
    
    #Copied the update function and changed slightly to work with bots
    def updatePlayPile(self, card_to_play):
        print(f"Bot {self.number} is playing a card...")
        print(f"Bot {self.number} Length of hand: {len(self.hand.cards)}")
        # remove top card from playPile
        self.game.playPile.removeWidget(self.game.top_card)
        # add card to top of playPile
        if card_to_play.number == "WILD":
            self.game.top_card = WildCard(self.game)
            self.game.top_card.setColor(card_to_play.color)
        elif card_to_play.number == "Skip":
            self.game.top_card = SkipCard(card_to_play.color, "Skip", self.game)
        elif card_to_play.number == "Reverse":
            self.game.top_card = ReverseCard(card_to_play.color, "Reverse", self.game)
        elif card_to_play.number == "Draw 2":
            self.game.top_card = DrawTwoCard(card_to_play.color, "Draw 2", self.game)
        else:
            self.game.top_card = Card(card_to_play.color, card_to_play.number, self.game)

        self.game.playPile.addWidget(self.game.top_card)