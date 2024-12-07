
from alt_backtest import indicator

class ExponentialMovingAverage(indicator.Indicator):
    lines = ('ema_line',)

    def __init__(self, period: int):
        super().__init__()
        self.period = period
        self.multiplier = 2 / (period + 1)
        self.ema = None

    def next(self):
        price = self.get_price()
        if self.ema is None:
            self.ema = price  # Первое значение EMA равно цене
        else:
            self.ema = (price - self.ema) * self.multiplier + self.ema
        self.lines.ema_line[0] = self.ema

    def is_ready(self) -> bool:
        return self.ema is not None
