from __future__ import print_function

from fxcarranza.backtest.backtest import Backtest
from fxcarranza.execution.execution import SimulatedExecution
from fxcarranza.portfolio.portfolio import Portfolio
from fxcarranza import settings
from fxcarranza.strategy.strategy import MovingAverageCrossStrategy
from fxcarranza.data.price import HistoricCSVPriceHandler


if __name__ == "__main__":
    # Trade on GBP/USD and EUR/USD
    pairs = ["GBPUSD", "EURUSD"]

    # Create the strategy parameters for the
    # MovingAverageCrossStrategy
    strategy_params = {
        "short_window": 500,
        "long_window": 2000
    }

    # Create and execute the backtest
    backtest = Backtest(
        pairs, HistoricCSVPriceHandler,
        MovingAverageCrossStrategy, strategy_params,
        Portfolio, SimulatedExecution,
        equity=settings.EQUITY
    )
    backtest.simulate_trading()
