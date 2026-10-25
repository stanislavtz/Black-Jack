import runpy
from pathlib import Path

import pytest
from constants import SEPARATOR
from models.card import Card
from models.deck import Deck
from models.player import Player
from models.table import Table
from main import check_for_ace, deal_cards, display_data, reduce_ace_value

MAIN_PATH = str(Path(__file__).with_name("main.py"))


def stack_deck(monkeypatch, cards):
    # deal() pops from the end, so the list is reversed to deal cards in the given order
    def fake_shuffle(self):
        self.deck = list(reversed(cards))

    monkeypatch.setattr(Deck, "shuffle_deck", fake_shuffle)


def play(monkeypatch, capsys, deal_order, answers):
    stack_deck(monkeypatch, deal_order)
    inputs = iter(["Alice", *answers])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    runpy.run_path(MAIN_PATH, run_name="__main__")
    return capsys.readouterr().out


def test_check_for_ace_is_true():
    cards_with_ace = [Card("Hearts", "Four"), Card("Diamonds", "Ace")]
    assert check_for_ace(cards_with_ace) == True


def test_check_for_ace_is_false():
    cards_without_ace = [Card("Hearts", "Four"), Card("Diamonds", "Two")]
    assert check_for_ace(cards_without_ace) == False


def test_check_for_ace_empty_hand_is_false():
    assert check_for_ace([]) == False


def test_check_for_ace_reduced_ace_is_false():
    reduced_ace = Card("Hearts", "Ace")
    reduced_ace.value = 1
    assert check_for_ace([Card("Clubs", "Two"), reduced_ace]) == False


def test_reduce_ace_value_reduces_first_ace_only():
    first_ace = Card("Hearts", "Ace")
    second_ace = Card("Spades", "Ace")
    hand = [Card("Clubs", "Nine"), first_ace, second_ace]

    reduce_ace_value(hand)

    assert first_ace.value == 1
    assert second_ace.value == 11
    assert hand[0].value == 9


def test_deal_cards_gives_two_cards_to_each_player_and_table(capsys):
    player = Player("Alice")
    table = Table()
    deck = Deck()
    deck.deck = [Card("Hearts", "Two"), Card("Clubs", "Three"), Card("Spades", "Four"), Card("Diamonds", "Five")]
    deck.deck.reverse()

    deal_cards([player], table, deck)

    assert len(player.cards) == 2
    assert len(table.cards) == 2
    assert SEPARATOR in capsys.readouterr().out


def test_deal_cards_deals_players_before_table():
    player = Player("Alice")
    table = Table()
    deck = Deck()
    deck.deck = [Card("Hearts", "Two"), Card("Clubs", "Three"), Card("Spades", "Four"), Card("Diamonds", "Five")]
    deck.deck.reverse()

    deal_cards([player], table, deck)

    assert [str(card) for card in player.cards] == ["Two of Hearts", "Three of Clubs"]
    assert [str(card) for card in table.cards] == ["Four of Spades", "Five of Diamonds"]


@pytest.mark.parametrize("participant_class", [Player, Table])
def test_display_data_prints_cards_and_value(participant_class, capsys):
    participant = Player("Alice") if participant_class is Player else Table()
    participant.cards = [Card("Hearts", "Ten"), Card("Clubs", "Seven")]

    display_data(participant)

    out = capsys.readouterr().out
    assert f"{participant.name}'s cards:" in out
    assert "Ten of Hearts" in out
    assert "Seven of Clubs" in out
    assert f"Current {participant.name} value:  17" in out


def test_play_blackjack_on_deal_player_wins(monkeypatch, capsys):
    out = play(
        monkeypatch,
        capsys,
        deal_order=[Card("Spades", "Ace"), Card("Hearts", "King"), Card("Clubs", "Two"), Card("Diamonds", "Three")],
        answers=[],
    )

    assert "BLACK JACK - The player wins!" in out


@pytest.mark.parametrize(
    "player_cards, table_cards, expected",
    [
        (("Ten", "Eight"), ("Ten", "Seven"), "Player wins!"),
        (("Ten", "Seven"), ("Ten", "Eight"), "Table wins!"),
        (("Ten", "Eight"), ("Ten", "Eight"), "Draft game!"),
    ],
)
def test_play_player_stands_and_higher_total_wins(monkeypatch, capsys, player_cards, table_cards, expected):
    out = play(
        monkeypatch,
        capsys,
        deal_order=[
            Card("Hearts", player_cards[0]), Card("Hearts", player_cards[1]),
            Card("Clubs", table_cards[0]), Card("Clubs", table_cards[1]),
        ],
        answers=["n"],
    )

    assert expected in out


def test_play_player_busts_without_ace_table_wins(monkeypatch, capsys):
    out = play(
        monkeypatch,
        capsys,
        deal_order=[
            Card("Hearts", "Ten"), Card("Hearts", "Eight"),
            Card("Clubs", "Ten"), Card("Clubs", "Seven"),
            Card("Spades", "King"),
        ],
        answers=["y"],
    )

    assert "BUSTED. The table wins!" in out
    assert "Reducing player's ACE" not in out


def test_play_player_busts_with_ace_reduces_and_continues(monkeypatch, capsys):
    out = play(
        monkeypatch,
        capsys,
        deal_order=[
            Card("Hearts", "Ten"), Card("Hearts", "Eight"),
            Card("Clubs", "Ten"), Card("Clubs", "Seven"),
            Card("Spades", "Ace"),
        ],
        answers=["y", "n"],
    )

    assert "Reducing player's ACE" in out
    assert "BUSTED" not in out
    assert "Player wins!" in out


def test_play_table_busts_without_ace_player_wins(monkeypatch, capsys):
    out = play(
        monkeypatch,
        capsys,
        deal_order=[
            Card("Hearts", "Ten"), Card("Hearts", "Eight"),
            Card("Clubs", "Ten"), Card("Clubs", "Six"),
            Card("Spades", "King"),
        ],
        answers=["n"],
    )

    assert "Table BUSTED. The player wins!" in out
    assert "Table wins!" not in out


def test_play_table_busts_with_ace_reduces_and_player_wins(monkeypatch, capsys):
    out = play(
        monkeypatch,
        capsys,
        deal_order=[
            Card("Hearts", "Ten"), Card("Hearts", "Eight"),
            Card("Clubs", "Ten"), Card("Clubs", "Six"),
            Card("Spades", "Ace"),
        ],
        answers=["n"],
    )

    assert "Reducing tables's ACE" in out
    assert "Table BUSTED" not in out
    assert "Player wins!" in out


def test_play_two_aces_on_deal_are_reduced(monkeypatch, capsys):
    out = play(
        monkeypatch,
        capsys,
        deal_order=[
            Card("Hearts", "Ace"), Card("Spades", "Ace"),
            Card("Clubs", "Ten"), Card("Clubs", "Seven"),
        ],
        answers=["n"],
    )

    assert "Reducing player's ACE" in out
    assert "Table wins!" in out

