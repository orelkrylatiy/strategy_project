
from alt_backtest import indicator, Price

class AverageTrueRange(indicator.Indicator):
    lines = ('atr',)

    def __init__(self, period: int):
        super().__init__()
        self.period = period
        self.tr_values = []
        self.close_prev = None

    def next(self):

        high = self.get_price(Price.high)
        low = self.get_price(Price.low)
        close = self.get_price(Price.close)

        if self.close_prev is None:
            self.close_prev = close
            return

        true_range = max(high - low, abs(high - self.close_prev), abs(low - self.close_prev))
        self.tr_values.append(true_range)

        if len(self.tr_values) > self.period:
            self.tr_values.pop(0)

        self.lines.atr[0] = sum(self.tr_values) / len(self.tr_values)

        self.close_prev = close

    def is_ready(self) -> bool:
        return len(self.tr_values) == self.period
