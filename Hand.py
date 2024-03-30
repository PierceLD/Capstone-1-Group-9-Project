import random
from Card import Card
from Card import WildCard

#Class to generate cards, will default to 7 cards when generating
class Hand():
    def __init__(self, size = 7):
        self.size = size
        self.cards = []
        self.generateCards(size)
    
    #Function will take an amount and generate that many cards, adding to hand
    def generateCards(self, size):
        colors = ['red', 'blue', 'green', 'yellow']
        for _ in range(size):
            random_number = random.randint(0, 9)
            if random.randint(0, 9) == 0: 
                card = WildCard("WILD")
            else:
                random_color = random.choice(colors)
                card = Card(random_color, random_number)
            card.in_hand = True
            self.cards.append(card)
    
    #Returns the cards in hand
    def getCards(self):
        return self.cards
    
    