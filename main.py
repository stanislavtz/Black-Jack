from constants import SEPARATOR
from models.deck import Deck
from models.table import Table
from models.player import Player


def deal_cards(players, table, deck):
    for player in players:
        player.draw_card(deck)
        player.draw_card(deck)

    print(SEPARATOR)

    table.draw_card(deck)
    table.draw_card(deck)


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


players = []

if __name__ == "__main__":
    table = Table()
    player1 = Player(input("Player name: "))
    players.append(player1)

    game_on = True

    print("!!! WELCOME TO BLACKJACK TABLE !!!")
    print(SEPARATOR)

    while game_on:
        deck = Deck()
        deck.shuffle_deck()

        deal_cards(players, table, deck)
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

                player1.draw_card(deck)
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
                table.draw_card(deck)
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
