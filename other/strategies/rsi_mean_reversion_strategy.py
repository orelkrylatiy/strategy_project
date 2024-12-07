from alt_backtest import strategy, position

from other.config import rsi_period, min_rsi, max_rsi
from other.indicators.rsi_indicator import RelativeStrengthIndex


class RSIMeanReversionStrategy(strategy.Strategy):
    def __init__(self):
        super().__init__()
        self.rsi = RelativeStrengthIndex(period=rsi_period)

    def next(self):
        if not self.rsi.is_ready():
            return
        if not self.in_position():
            if self.rsi.rsi[0] <= min_rsi:
                self.send_market_order_buy()
                self.position_status = position.Position.long
                return
            elif self.rsi.rsi[0] >= max_rsi:
                self.send_market_order_sell()
                self.position_status = position.Position.short
            return

        if self.position_status == position.Position.long:
            if self.rsi.rsi[0] >= 50:
                self.send_market_order_sell()
                self.position_status = position.Position.none
                return
        if self.position_status == position.Position.short:
            if self.rsi.rsi[0] <= 50:
                self.send_market_order_buy()
                self.position_status = position.Position.none