import math
import pytest

from calculator import evaluate, SafeEvaluator


def test_addition():
    assert evaluate("2 + 3") == 5


def test_subtraction():
    assert evaluate("10 - 4") == 6


def test_multiplication():
    assert evaluate("6 * 7") == 42


def test_division():
    assert evaluate("8 / 2") == 4


def test_precedence():
    assert evaluate("2 + 3 * 4") == 14


def test_parentheses():
    assert evaluate("(2 + 3) * 4") == 20


def test_unary_minus():
    assert evaluate("-(5)") == -5


def test_unary_plus():
    assert evaluate("+5") == 5


def test_float_result():
    assert math.isclose(evaluate("7 / 2"), 3.5)


def test_whitespace_handling():
    assert evaluate("  1 +    1 ") == 2


def test_invalid_name():
    with pytest.raises(ValueError):
        evaluate("x + 1")


def test_invalid_call():
    with pytest.raises(ValueError):
        SafeEvaluator().evaluate_expression("(1).__class__")


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate("1 / 0")