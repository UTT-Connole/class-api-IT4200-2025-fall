import pytest
from app import get_payout  

def test_get_payout_number_win():
    assert get_payout("number", 7, 7, "red") == 35

def test_get_payout_number_loss():
    assert get_payout("number", 7, 3, "black") == -1

def test_get_payout_color_win():
    assert get_payout("color", "red", 5, "red") == 1

def test_get_payout_color_loss():
    assert get_payout("color", "red", 5, "black") == -1

def test_get_payout_invalid_bet_type():
    assert get_payout("invalid", "red", 5, "black") == -1

def test_get_payout_case_insensitive_color():
    assert get_payout("color", "Red", 5, "rEd") == 1
