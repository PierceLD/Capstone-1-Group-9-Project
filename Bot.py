from time import sleep
import random
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Hand import Hand
from Card import Card

class Bot():
    #Starts the bot player with a hand of 7 and no score
    def __init__(self, game_board):
        super().__init__()
        self.game = game_board
        self.hand = Hand()
        self.score = 0

    #Looks for a playable card. If none are found, draw a card instead and return None
    #If we want, we can add some stradegy by having it do lowest first and basing it's chance on that
    def canPlayCard(self, color, number):
        for i in self.hand.cards:
            if i.color == color or i.number == number:
                return i
        self.drawCard
        return None
            
    #Adds a random card to the hand
    def drawCard(self):
        self.hand.cards.append(self.genRandomCard())

    #Updates the game_Board with the properly chosen card
    def playCard(self):
        #The chance the bot gets it right based off the card num
        top_card = self.game.top_card
        card_to_play = self.canPlayCard(top_card.color, top_card.number)

        if card_to_play == None:
            print("Bot has no playable cards. Drawing for bot...")
            self.drawCard
        elif random.random() < (1 - (card_to_play.number/100)):
            self.updatePlayPile(card_to_play)
            self.hand.cards.remove(card_to_play)
            self.score += 1
            print(f"Bot playing {card_to_play.color} {card_to_play.number}")
        else:
            print("Bot did not get it right")

    #Copied the gen function over to not have circular import
    def genRandomCard(self):
        colors = ['red', 'blue', 'green', 'yellow']
        random_number = random.randint(0, 9)
        random_color = random.choice(colors)
        return Card(random_color, random_number)
    
    #Copied the update function and changed slightly to work with bots
    def updatePlayPile(self, card_to_play):
        print("Bot is playing a card...")
        print(f"Bot Length of hand: {len(self.hand.cards)}")
        # remove top card from playPile
        self.game.playPile.removeWidget(self.game.top_card)
        # add card to top of playPile
        self.game.top_card = Card(card_to_play.color, card_to_play.number)
        self.game.top_card.question = card_to_play.question
        self.game.playPile.addWidget(self.game.top_card)