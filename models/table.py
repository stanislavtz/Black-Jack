class Table:
    def __init__(self):
        self.name = "Table"
        self.cards = []

    def draw_card(self, deck):
        print(f"{self.name} draws card!")
        self.cards.append(deck.deal())

    def drawn_cards_values(self):
        return sum(card.value for card in self.cards)

    def print_some_cards(self):
        print("Table's initial cards:")
        print(self.cards[0])
        print("HIDDEN")

    def print_cards(self):
        print(f"{self.name}'s cards:")
        [print(card) for card in self.cards]