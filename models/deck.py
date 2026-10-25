import random
from constants import suits, ranks
from models.card import Card


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.deck.append(card)

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

    def __str__(self):
        print("Deck list:")
        cards = [str(card) for card in self.deck]
        return "\n".join(cards)