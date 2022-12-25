from __future__ import annotations

from decimal import Decimal
from typing import Final
import math


class InvalidProbabilityRange(Exception):
    """Vanilla exception for invalid probability ranges and values."""
    pass


class InvalidEncodeInput(Exception):
    """Vanilla Exception for invalid decoder input."""
    pass


class ArithmeticCoder:
    """Defines arithmeic coding class."""

    def __init__(self, symbols_prob: dict[str, Decimal]) -> None:
        """
        Initializes the class.
        Args:
            symbols_prob: dict from symbol to its probability
        """
        self.symbols_prob: Final[dict[str, Decimal]] = symbols_prob
        self._sanity_check_inputs()
        # python 3.6+ dicts are ordered in the way keys are inserted
        self.current_sym_ranges: dict[str, tuple[Decimal, Decimal]] = {}
        self._update_symbol_ranges(Decimal("0.0"), Decimal("1.0"))

    def _update_symbol_ranges(self, start: Decimal, end: Decimal):
        """
        For a given range, get symbol codes new prob-ranges.
        """
        # basic formula is sym_start + prob*range_available
        prev_start = start
        prob_range = end - start
        for idx, key in enumerate(self.symbols_prob.keys()):
            prev_end = prev_start + self.symbols_prob[key] * prob_range
            self.current_sym_ranges[key] = (prev_start, prev_end)
            if idx == len(self.symbols_prob) - 1:
                self.current_sym_ranges[key] = (prev_start, Decimal(end))
            prev_start = prev_end
        return start, end

    def _sanity_check_inputs(self) -> None:
        """Checks if the input probability distrubution sums to 1.0."""
        cum_sum_prob = Decimal("0.0")
        for key, val in self.symbols_prob.items():
            cum_sum_prob += val
        if not math.isclose(cum_sum_prob, Decimal("1.0"), rel_tol=1e-5):
            raise InvalidProbabilityRange(
                {"Message: Inavlid probability value and range in input."})

    def encode(self, message: str) -> Decimal:
        """
        Encodes a given message.
        """
        # loop through chars of the message to be encoded
        #  next range would be the range from the current range for the first char
        #  subsequently range would get updated with every element

        for idx, sym in enumerate(message):
            try:
                cur_sym_ranges = self.current_sym_ranges[sym]
            except KeyError:
                raise InvalidEncodeInput({
                    "The symbol provided to encode does not exist in codebook: {sym}"
                })
            code_start, code_end = self._update_symbol_ranges(*cur_sym_ranges)
        mid_pt: Final = Decimal("0.5")
        return mid_pt * (code_start + code_end)

    def _get_symbol_from_current_ranges(self, val: Decimal) -> str:
        for key, ar_range in self.current_sym_ranges.items():
            if ar_range[0] < val and ar_range[1] >= val:
                return key
        raise ValueError("Error")

    def decode(self, message_length: int, numeric_code: Decimal) -> str:
        """
        Decodes a message.
        """
        # constructs initial ranges using probabilities
        # keep partitioning until reach the length
        self._update_symbol_ranges(Decimal("0.0"), Decimal("1.0"))
        print(f"cur: {self.current_sym_ranges}")
        levels = message_length - 1
        current_msg_dec_val = numeric_code
        output_msg = []
        while levels >= 0:
            key = self._get_symbol_from_current_ranges(current_msg_dec_val)
            levels -= 1
            self._update_symbol_ranges(*self.current_sym_ranges[key])
            output_msg.append(key)
        assert len(
            output_msg
        ) == message_length, "Weirdly length of decoded symbol do not match to the expected mesage length."
        return "".join(output_msg)
