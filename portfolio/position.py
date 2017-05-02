from decimal import Decimal, getcontext, ROUND_HALF_DOWN


class Position(object):
    CONTRACT_SIZE = Decimal("100000.00")

    def __init__(
        self, home_currency, position_type, 
        currency_pair, units, ticker,
        take_profit, stop_loss
    ):
        self.home_currency = home_currency  # Account denomination (e.g. GBP)
        self.position_type = position_type  # Long or short
        self.currency_pair = currency_pair  # Intended traded currency pair
        self.units = units
        self.ticker = ticker
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.set_up_currencies()
        self.pip_value = self.calculate_pip_value()
        self.profit_base = self.calculate_profit_base()
        self.profit_perc = self.calculate_profit_perc()

    def set_up_currencies(self):
        ticker_cur = self.ticker.prices[self.currency_pair]
        if self.position_type == "long":
            self.avg_price = Decimal(str(ticker_cur["ask"]))
            self.cur_price = Decimal(str(ticker_cur["bid"]))    
        else:
            self.avg_price = Decimal(str(ticker_cur["bid"]))
            self.cur_price = Decimal(str(ticker_cur["ask"]))

    def calculate_pips(self):
        mult = Decimal("1")
        if self.position_type == "long":
            mult = Decimal("1")
        elif self.position_type == "short":
            mult = Decimal("-1")
        pips = (mult * (self.cur_price - self.avg_price)) * Decimal("10000")
        return pips

    def calculate_pip_value(self):
        if self.currency_pair[-3:] == 'USD':
            return Decimal("0.0001") * self.units
        else:
            pip_value = Decimal("0.0001") * self.units / self.avg_price
            return pip_value.quantize(Decimal("0.01", ROUND_HALF_DOWN))

    def calculate_profit_base(self):
        pips = self.calculate_pips()
        ticker = self.ticker.prices[self.currency_pair]
        if self.position_type == "long":
            close = ticker["bid"]
        else:
            close = ticker["ask"]
        profit = pips * self.pip_value
        return profit.quantize(
            Decimal("0.00001"), ROUND_HALF_DOWN
        )   

    def calculate_profit_perc(self):
        return (self.profit_base / self.units * Decimal("100.00")).quantize(
            Decimal("0.00001"), ROUND_HALF_DOWN
        )

    def update_position_price(self):
        ticker_cur = self.ticker.prices[self.currency_pair]
        if self.position_type == "long":
            self.cur_price = Decimal(str(ticker_cur["bid"]))
        else:
            self.cur_price = Decimal(str(ticker_cur["ask"]))
        self.profit_base = self.calculate_profit_base()
        self.profit_perc = self.calculate_profit_perc()

    def add_units(self, units):
        cp = self.ticker.prices[self.currency_pair]
        if self.position_type == "long":
            add_price = cp["ask"]
        else:
            add_price = cp["bid"]
        new_total_units = self.units + units
        new_total_cost = self.avg_price * self.units + add_price * units
        self.avg_price = new_total_cost / new_total_units
        self.units = new_total_units
        self.update_position_price()

    def remove_units(self, units):
        dec_units = Decimal(str(units))
        cp = self.ticker.prices[self.currency_pair]
        if self.position_type == "long":
            remove_price = cp["bid"]
            close = cp["ask"]
        else:
            remove_price = cp["ask"]
            close = cp["bid"]
        self.units -= dec_units
        self.update_position_price()
        # Calculate PnL
        pnl = self.calculate_pips() * close * dec_units
        getcontext().rounding = ROUND_HALF_DOWN
        return pnl.quantize(Decimal("0.01"))

    def close_position(self):
        cp = self.ticker.prices[self.currency_pair]
        if self.position_type == "long":
            close = cp["ask"]
        else:
            close = cp["bid"]
        self.update_position_price()
        # Calculate PnL
        pnl = self.calculate_pips() * close * self.units
        getcontext().rounding = ROUND_HALF_DOWN
        return pnl.quantize(Decimal("0.01"))
