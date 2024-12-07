
from alt_backtest import indicator
from MAX_strategy. max_indicators. ema_indicator import ExponentialMovingAverage


class MovingAverageConvergenceDivergence(indicator.Indicator):
    lines = ('macd',)

    def __init__(self, long_period: int, short_period: int):
        super().__init__()
        self.long_period = long_period
        self.short_period = short_period
        self.short_ema = ExponentialMovingAverage(period=short_period)
        self.long_ema = ExponentialMovingAverage(period=long_period)

    def next(self):
        self.lines.macd[0] = self.short_ema.ema_line[0] - self.long_ema.ema_line[0]

    def is_ready(self) -> bool:
        return self.short_ema.is_ready() and self.long_ema.is_ready()
