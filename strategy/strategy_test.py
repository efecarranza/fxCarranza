from decimal import Decimal
import unittest

from strategy import MovingAverageCrossStrategy

# =====================================
# GBP Home Currency with GBP/USD traded
# =====================================

class TestHelperMethods(unittest.TestCase):
    """
    Unit tests for helper methods used in calculations
    """
    def setUp(self):
        pairs = {}
        events = {}
        short_window = 9
        long_window = 18
        self.strategy = MovingAverageCrossStrategy(
            pairs, events, short_window, long_window
        )

    def test_get_multiplier_with9window(self):
        multiplier = self.strategy.get_multiplier(9)
        self.assertEquals(Decimal("0.2000"), multiplier)

    def test_get_multiplier_with10window(self):
        multiplier = self.strategy.get_multiplier(10)
        self.assertEquals(Decimal("0.1818"), multiplier)


if __name__ == "__main__":
    unittest.main()
