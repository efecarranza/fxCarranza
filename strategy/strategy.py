import copy
from decimal import Decimal, getcontext, ROUND_HALF_DOWN

from fxcarranza.event.event import SignalEvent
from fxcarranza.database.connection import DBConnection

class MovingAverageCrossStrategy(object):
    """
    A trading strategy determining whether we should be in a buying
    or in a selling period.
    """
    def __init__(
        self, pairs, events,
        short_window=9, long_window=18
    ):
        self.pairs = pairs
        self.pairs_dict = self.create_pairs_dict()
        self.events = events
        self.short_window = short_window
        self.long_window = long_window
        self.short_ema = self.calculate_initial_ema(short_window)
        self.long_ema = self.calculate_initial_ema(long_window)

    def create_pairs_dict(self):
        attr_dict = {
            "ticks": 0,
            "invested": False,
            "short_sma": None,
            "long_sma": None
        }
        pairs_dict = {}
        for p in self.pairs:
            pairs_dict[p] = copy.deepcopy(attr_dict)
        return pairs_dict

    def calculate_initial_ema(self, window):
        initial_total = 0
        multiplier = self.get_multiplier(window)

        conn = DBConnection()
        prices = conn.get_historical_prices("eurusd", window)

        sma = self.get_sma(prices, window)
        latest_close = prices[0][1]

        ema = ((Decimal(latest_close) - sma) * multiplier) + sma

        return ema

    def calc_rolling_ema(self, current_ema, window, price):
        multiplier = self.get_multiplier(window)
        ema = ((Decimal(price) - current_ema) * multiplier) + current_ema

        return Decimal(ema.quantize(Decimal(".0001"), ROUND_HALF_DOWN))


    def calculate_signals(self, event):
        if event.type == 'TICK':
            pair = event.instrument
            price = event.bid
            pd = self.pairs_dict[pair]
            if pd["ticks"] == 0:
                pd["short_sma"] = price
                pd["long_sma"] = price
            else:
                pd["short_sma"] = self.calc_rolling_sma(
                    pd["short_sma"], self.short_window, price
                )
                pd["long_sma"] = self.calc_rolling_sma(
                    pd["long_sma"], self.long_window, price
                )
            # Only start the strategy when we have created an accurate short window
            if pd["ticks"] > self.short_window:
                if pd["short_sma"] > pd["long_sma"] and not pd["invested"]:
                    signal = SignalEvent(pair, "market", "buy", event.time)
                    self.events.put(signal)
                    pd["invested"] = True
                if pd["short_sma"] < pd["long_sma"] and pd["invested"]:
                    signal = SignalEvent(pair, "market", "sell", event.time)
                    self.events.put(signal)
                    pd["invested"] = False
            pd["ticks"] += 1

    def get_multiplier(self, window):
        multiplier = Decimal(2.0 / (window + 1))
        return Decimal(multiplier.quantize(Decimal(".0001"), ROUND_HALF_DOWN))

    def get_sma(self, prices, window):
        initial_total = 0
        for price in prices:
            initial_total += price[1]

        sma = Decimal(initial_total / window)

        return Decimal(sma.quantize(Decimal(".0001"), ROUND_HALF_DOWN))
