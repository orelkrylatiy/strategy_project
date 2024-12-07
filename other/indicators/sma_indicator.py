from alt_backtest import indicator


class SimpleMovingAverage(indicator.Indicator):
    lines = ('sma',)

    def __init__(self, period: int):
        super().__init__()
        self.period = period
        self.mass = []

    def next(self):
        self.dataclose = self.get_price()
        if len(self.mass) ==self.period:
            self.mass.pop(0)
        self.mass.append(self.dataclose)
        self.lines.sma[0] = sum(self.mass) / len(self.mass)

    def is_ready(self) -> bool:
        return len(self.mass) == self.period