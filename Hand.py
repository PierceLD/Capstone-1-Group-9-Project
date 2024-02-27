import random
from Card import Card

#Class to generate cards, will default to 7 cards when generating
class Hand():
    def __init__(self, size = 7):
        self.size = size
        self.cards = []
        self.generate_cards(size)
    
    #Function will take an amount and generate that many cards, adding to hand
    def generate_cards(self, amount):
        colors = ['red', 'blue', 'green', 'yellow']
        for _ in range(amount):
            random_number = random.randint(0, 9)
            random_color = random.choice(colors)
            card = Card(random_color, random_number)
            self.cards.append(card)
    
    #Returns the cards in hand
    def get_cards(self):
        return self.cards
    
    