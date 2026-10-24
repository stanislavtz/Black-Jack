import random

SEPARATOR = "=" * 50
suits = ("Hearths", "Diamonds", "Clubs", "Spades")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2,"Three": 3,"Four": 4,"Five": 5,"Six": 6,"Seven": 7,"Eight": 8,"Nine": 9,"Ten": 10,"Jack": 10,"Queen": 10,
    "King": 10,"Ace": 11}
players = []


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


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


class Table:
    def __init__(self):
        self.name = "Table"
        self.cards = []

    def draw_card(self):
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


class Player(Table):
    def __init__(self, name):
        super().__init__()
        self.name = name


def deal_cards(players, table):
    for player in players:
        player.draw_card()
        player.draw_card()

    print(SEPARATOR)

    table.draw_card()
    table.draw_card()


def display_data(player):
    player.print_cards()
    value = player.drawn_cards_values()
    print(f"Current {player.name} value: ", value)


def check_for_ace(cards):
    has_ace = False
    for card in cards:
        if card.value == 11:
            has_ace = True
            break
    return has_ace


def reduce_ace_value(cards):
    ace_card = [card for card in cards if card.value == 11]
    ace_card[0].value = 1


table = Table()
player1 = Player(input("Player name: "))
players.append(player1)

game_on = True

print("!!! WELCOME TO BLACKJACK TABLE !!!")
print(SEPARATOR)

while game_on:
    deck = Deck()
    deck.shuffle_deck()

    deal_cards(players, table)
    print(SEPARATOR)

    display_data(player1)
    player_value = player1.drawn_cards_values()
    print(SEPARATOR)

    table.print_some_cards()
    table_value = table.cards[0].value
    print(f"Current {table.name} value: ", table_value)
    print(SEPARATOR)

    if player_value == 21:
        print("BLACK JACK - The player wins!")
        game_on = False
        continue
    elif player_value < 21:
        answer = "y"
        while answer[0].lower() == "y":
            answer = input(f"{player1.name} would you like to draw a card? y/n: ")
            if answer[0].lower() != "y":
                break

            player1.draw_card()
            display_data(player1)
            player_value = player1.drawn_cards_values()
            print(SEPARATOR)

            if player_value > 21:
                if check_for_ace(player1.cards):
                    print("Reducing player's ACE")
                    reduce_ace_value(player1.cards)
                    display_data(player1)
                    player_value = player1.drawn_cards_values()
                    continue
                print(f"Player {player1.name} BUSTED. The table wins!")
                game_on = False
                break

    if game_on:
        print(SEPARATOR)
        display_data(table)
        table_value = table.drawn_cards_values()
        print(SEPARATOR)

        while table_value < 17:
            table.draw_card()
            display_data(table)
            table_value = table.drawn_cards_values()
            print(SEPARATOR)
            if table_value > 21:
                if check_for_ace(table.cards):
                    print("Reducing tables's ACE")
                    reduce_ace_value(table.cards)
                    display_data(table)
                    table_value = table.drawn_cards_values()
                    print(SEPARATOR)
                else:
                    print("Table BUSTED. The player wins!")
                    game_on = False
                    break

        if table_value > player_value:
            print("Table wins!")
            game_on = False
        elif table_value < player_value:
            print("Player wins!")
            game_on = False
        else:
            print("Draft game!")
            game_on = False

