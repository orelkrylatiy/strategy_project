from alt_backtest import strategy, position

from other.config import sma_period, sma_period_small
from other.indicators.sma_indicator import SimpleMovingAverage



class Trend2SMAStrategy(strategy.Strategy):
    def __init__(self):
        super().__init__()
        self.sma = SimpleMovingAverage(period=sma_period)
        self.sma_small = SimpleMovingAverage(period=sma_period_small)
        self.sma_value = 0
        self.sma_value_small = 0

    def next(self):
        if not self.sma.is_ready():
            return
        if not self.in_position():
            if self.sma_value >= self.sma_value_small and self.sma.sma[0] < self.sma_small.sma[0]:
                self.send_market_order_buy()
                self.position_status = position.Position.long
                self.set_current_value()
                return
            elif self.sma_value <= self.sma_value_small and self.sma.sma[0] > self.sma_small.sma[0]:
                self.send_market_order_sell()
                self.position_status = position.Position.short
            self.set_current_value()
            return

        if self.position_status == position.Position.long:
            if self.sma_value <= self.sma_value_small and self.sma.sma[0] > self.sma_small.sma[0]:
                self.send_market_order_sell()
                self.position_status = position.Position.none
                self.set_current_value()
                return
        if self.position_status == position.Position.short:
            if self.sma_value >= self.sma_value_small and self.sma.sma[0] < self.sma_small.sma[0]:
                self.send_market_order_buy()
                self.position_status = position.Position.none
        self.set_current_value()

    def set_current_value(self):
        self.sma_value = self.sma.sma[0]
        self.sma_value_small = self.sma_small.sma[0]