from __future__ import annotations

import pytest

from arithmetic_coder import ArithmeticCoder, InvalidProbabilityRange, InvalidEncodeInput
import math
from decimal import Decimal


def test_invalid_inputs() -> None:
    test_symbol_prob: dict[str, Decimal] = {
        "a": Decimal("0.2"),
        "b": Decimal("0.7"),
        "c": Decimal("0.2")
    }
    with pytest.raises(InvalidProbabilityRange):
        ArithmeticCoder(test_symbol_prob)


def test_invalid_decoding() -> None:
    test_symbol_prob: dict[str, Decimal] = {
        "a": Decimal("0.2"),
        "b": Decimal("0.7"),
        "c": Decimal("0.1")
    }
    acoder = ArithmeticCoder(test_symbol_prob)
    with pytest.raises(InvalidEncodeInput):
        acoder.encode("addd")


def test_valid_encoding_decoding() -> None:
    test_symbol_prob: dict[str, Decimal] = {
        "a": Decimal("0.2"),
        "b": Decimal("0.7"),
        "c": Decimal("0.1")
    }
    acoder = ArithmeticCoder(test_symbol_prob)
    msg = "abc"
    encoded = acoder.encode(msg)
    assert math.isclose(encoded, Decimal("0.1730"))
    decoded = acoder.decode(len(msg), encoded)
    assert decoded == msg


def test_e2e() -> None:
    test_symbol_prob: dict[str, Decimal] = {
        "a": Decimal("0.2"),
        "b": Decimal("0.3"),
        "c": Decimal("0.1"),
        "d": Decimal("0.4")
    }
    msg = "bda"
    acoder = ArithmeticCoder(test_symbol_prob)
    decoded = acoder.decode(len(msg), acoder.encode(msg))
    assert msg == decoded

    msg = "cdccba"
    acoder = ArithmeticCoder(test_symbol_prob)
    decoded = acoder.decode(len(msg), acoder.encode(msg))
    assert msg == decoded
