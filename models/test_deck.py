from models.deck import Deck
deck = Deck()

def test_deck_contains_52_cards():
    assert len(deck.deck) == 52


def test_deck_shuffle_mixes_the_cards():
    deck.shuffle_deck()
    while deck.deck[0].value == 2:
        deck.shuffle_deck()
    assert len(deck.deck) == 52 and deck.deck[0].value != 2


def test_deck_deal():
    deck.deal()
    assert len(deck.deck) == 51


def test_deck_string_value():
    new_deck = Deck()
    assert str(new_deck).startswith("Two of Hearts") == True
