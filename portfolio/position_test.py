from decimal import Decimal
import unittest

from position import Position


class TickerMock(object):
    """
    A mock object that allows a representation of the
    ticker/pricing handler.
    """

    def __init__(self):
        self.pairs = ["GBPUSD", "EURUSD"]
        self.prices = {
            "GBPUSD": {"bid": Decimal("1.50328"), "ask": Decimal("1.50349")},
            "EURUSD": {"bid": Decimal("1.07832"), "ask": Decimal("1.07847")}
        }



# =====================================
# GBP Home Currency with GBP/USD traded
# =====================================

class TestLongGBPUSDPosition(unittest.TestCase):
    """
    Unit tests that cover going long GBP/USD with an account
    denominated currency of GBP, using 2,000 units of GBP/USD.
    """
    def setUp(self):
        home_currency = "USD"
        position_type = "long"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()
        self.position = Position(
            home_currency, position_type, 
            currency_pair, units, ticker
        )

    def test_calculate_init_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-2.100"))

    def test_calculate_init_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-0.42000"))

    def test_calculate_init_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.02100"))

    def test_calculate_updated_values(self):
        """
        Check that after the bid/ask prices move, that the updated
        pips, profit and percentage profit calculations are correct.
        """
        prices = self.position.ticker.prices
        prices["GBPUSD"] = {"bid": Decimal("1.50486"), "ask": Decimal("1.50586")}
        self.position.update_position_price()

        # Check pips
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("13.7000"))
        # Check profit base
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("2.74000"))
        # Check profit percentage
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("0.1370"))


class TestShortGBPUSDPosition(unittest.TestCase):
    """
    Unit tests that cover going short GBP/USD with an account
    denominated currency of GBP, using 2,000 units of GBP/USD.
    """
    def setUp(self):
        home_currency = "USD"
        position_type = "short"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()
        self.position = Position(
            home_currency, position_type, 
            currency_pair, units, ticker
        )

    def test_calculate_init_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-2.1000"))

    def test_calculate_init_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-0.4200"))

    def test_calculate_init_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.02100"))

    def test_calculate_updated_values(self):
        """
        Check that after the bid/ask prices move, that the updated
        pips, profit and percentage profit calculations are correct.
        """
        prices = self.position.ticker.prices
        prices["GBPUSD"] = {"bid": Decimal("1.50486"), "ask": Decimal("1.50586")}
        self.position.update_position_price()

        # Check pips
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-25.80000"))
        # Check profit base
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-5.16000"))
        # Check profit percentage
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.25800"))


# =====================================
# GBP Home Currency with EUR/USD traded
# =====================================

class TestLongEURUSDPosition(unittest.TestCase):
    """
    Unit tests that cover going long EUR/USD with an account
    denominated currency of GBP, using 2,000 units of EUR/USD.
    """
    def setUp(self):
        home_currency = "USD"
        position_type = "long"
        currency_pair = "EURUSD"
        units = Decimal("2000")
        ticker = TickerMock()
        self.position = Position(
            home_currency, position_type, 
            currency_pair, units, ticker
        )

    def test_calculate_init_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-1.5000"))

    def test_calculate_init_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-0.30000"))

    def test_calculate_init_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.01500"))

    def test_calculate_updated_values(self):
        """
        Check that after the bid/ask prices move, that the updated
        pips, profit and percentage profit calculations are correct.
        """
        prices = self.position.ticker.prices
        prices["EURUSD"] = {"bid": Decimal("1.07811"), "ask": Decimal("1.07827")}
        self.position.update_position_price()

        # Check pips
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-3.60000"))
        # Check profit base
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-0.72000"))
        # Check profit percentage
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.03600"))


class TestShortEURUSDPosition(unittest.TestCase):
    """
    Unit tests that cover going short EUR/USD with an account
    denominated currency of GBP, using 2,000 units of EUR/USD.
    """
    def setUp(self):
        home_currency = "USD"
        position_type = "short"
        currency_pair = "EURUSD"
        units = Decimal("2000")
        ticker = TickerMock()
        self.position = Position(
            home_currency, position_type, 
            currency_pair, units, ticker
        )

    def test_calculate_init_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-1.50000"))

    def test_calculate_init_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-0.30000"))

    def test_calculate_init_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.01500"))

    def test_calculate_updated_values(self):
        """
        Check that after the bid/ask prices move, that the updated
        pips, profit and percentage profit calculations are correct.
        """
        prices = self.position.ticker.prices
        prices["EURUSD"] = {"bid": Decimal("1.07811"), "ask": Decimal("1.07827")}
        self.position.update_position_price()

        # Check pips
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("0.50000"))
        # Check profit base
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("0.10000"))
        # Check profit percentage
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("0.00500"))


if __name__ == "__main__":
    unittest.main()