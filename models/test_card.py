import pytest
from models.card import Card


def test_card_stores_suit_and_rank():
    card = Card("Spades", "Queen")
    assert card.suit == "Spades"
    assert card.rank == "Queen"


@pytest.mark.parametrize(
    "rank, expected_value",
    [
        ("Two", 2), ("Three", 3), ("Four", 4), ("Five", 5), ("Six", 6),
        ("Seven", 7), ("Eight", 8), ("Nine", 9), ("Ten", 10),
        ("Jack", 10), ("Queen", 10), ("King", 10), ("Ace", 11),
    ],
)
def test_card_value_for_each_rank(rank, expected_value):
    assert Card("Clubs", rank).value == expected_value


def test_card_str_returns_rank_of_suit():
    assert str(Card("Diamonds", "Seven")) == "Seven of Diamonds"


def test_card_str_for_ace():
    assert str(Card("Hearts", "Ace")) == "Ace of Hearts"


def test_card_str_of_king():
    assert str(Card("Hearts", "King")) == "King of Hearts"


def test_card_with_unknown_rank_raises_key_error():
    with pytest.raises(KeyError, match="Joker"):
        Card("Hearts", "Joker")
