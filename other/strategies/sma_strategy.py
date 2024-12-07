from alt_backtest import strategy, position

from other.config import sma_period
from other.indicators.sma_indicator import SimpleMovingAverage


class SMAStrategy(strategy.Strategy):
    def __init__(self):
        super().__init__()
        self.sma = SimpleMovingAverage(period=sma_period)

    def next(self):
        if not self.sma.is_ready():
            return
        if not self.in_position():
            if self.get_price() > self.sma.sma[0]:
                self.send_market_order_buy()
                self.position_status = position.Position.long
                return
            elif self.get_price() < self.sma.sma[0]:
                self.send_market_order_sell()
                self.position_status = position.Position.short
            return

        if self.position_status == position.Position.long:
            if self.get_price() < self.sma.sma[0]:
                self.send_market_order_sell()
                self.position_status = position.Position.none
                return
        if self.position_status == position.Position.short:
            if self.get_price() > self.sma.sma[0]:
                self.send_market_order_buy()
                self.position_status = position.Position.none