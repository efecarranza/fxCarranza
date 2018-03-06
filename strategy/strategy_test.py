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

    def test_calc_rolling_ema_window_9(self):
        current_ema = Decimal("1.2000")
        window = 9
        rolling_ema = self.strategy.calc_rolling_ema(current_ema, window, "1.2100")
        self.assertEquals(rolling_ema, Decimal("1.2020"))

    def test_calc_rolling_ema_window_10(self):
        current_ema = Decimal("1.2000")
        window = 10
        rolling_ema = self.strategy.calc_rolling_ema(current_ema, window, "1.2100")
        self.assertEquals(rolling_ema, Decimal("1.2018"))

if __name__ == "__main__":
    unittest.main()
