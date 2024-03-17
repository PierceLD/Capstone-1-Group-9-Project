import random
from Card import Card

#Class to generate cards, will default to 7 cards when generating
class Hand():
    def __init__(self, size = 7):
        self.size = size
        self.cards = []
        self.generate_cards(size)
    
    #Function will take an amount and generate that many cards, adding to hand
    def generate_cards(self, size):
        colors = ['red', 'blue', 'green', 'yellow']
        for _ in range(size):
            random_number = random.randint(0, 9)
            random_color = random.choice(colors)
            card = Card(random_color, random_number)
            card.in_hand = True
            self.cards.append(card)
    
    #Returns the cards in hand
    def get_cards(self):
        return self.cards
    
    