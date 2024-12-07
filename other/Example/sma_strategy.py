from alt_backtest import strategy, position

from config import sma_period
from other.indicators.sma_indicator import SimpleMovingAverage


class SMAStrategy(strategy.Strategy):
    order = None
    def __init__(self):
        super().__init__()
        self.sma = SimpleMovingAverage(period=sma_period)
        self.order = None

    def next(self):
        if not self.sma.is_ready():
            return
        if not self.in_position():
            if self.get_price() > self.sma.sma[0]:
                self.order = self.send_market_order_buy(size=2)
                self.position_status = position.Position.long
                return
            if self.get_price() < self.sma.sma[0]:
                self.order = self.send_market_order_sell(size=2)
                self.position_status = position.Position.short
            return


        if self.position_status == position.Position.long:
            if self.get_price() < self.sma.sma[0]:
                self.send_market_order_sell(size=2)
                self.position_status = position.Position.none
                return
        if self.position_status == position.Position.short:
                if self.get_price() > self.sma.sma[0]:
                    self.send_market_order_buy(size=2)
                    self.position_status = position.Position.none