"""Small quantity parsers for a fictional cookbook teaching example."""

import re
from fractions import Fraction


DECIMAL = re.compile(r"[0-9]+(?:\.[0-9]+)?")
FRACTION = re.compile(r"([0-9]+)/([0-9]+)")
MIXED = re.compile(r"([0-9]+) +([0-9]+)/([0-9]+)")


def _text(value):
    if not isinstance(value, str):
        raise TypeError("Quantity must be text")
    return value.strip()


def baseline(value):
    """Accept nonnegative integer and decimal quantities only."""
    text = _text(value)
    if DECIMAL.fullmatch(text):
        return Fraction(text)
    raise ValueError("Unsupported quantity")


def candidate(value):
    """Also accept fractions and mixed numbers, without interpreting units."""
    text = _text(value)
    if DECIMAL.fullmatch(text):
        return Fraction(text)
    match = FRACTION.fullmatch(text)
    if match:
        numerator, denominator = map(int, match.groups())
        if denominator > 0:
            return Fraction(numerator, denominator)
    match = MIXED.fullmatch(text)
    if match:
        whole, numerator, denominator = map(int, match.groups())
        if 0 < numerator < denominator:
            return Fraction(whole) + Fraction(numerator, denominator)
    raise ValueError("Unsupported quantity")
