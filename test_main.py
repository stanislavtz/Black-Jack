import pytest
from models.card import Card
from main import check_for_ace


def test_check_for_ace_is_true():
    cards_with_ace = [Card("Hearts", "Four"), Card("Diamonds", "Ace")]
    assert check_for_ace(cards_with_ace) == True


def test_check_for_ace_is_false():
    cards_without_ace = [Card("Hearts", "Four"), Card("Diamonds", "Two")]
    assert check_for_ace(cards_without_ace) == False

