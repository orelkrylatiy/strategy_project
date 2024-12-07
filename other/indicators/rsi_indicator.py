from alt_backtest import indicator


class RelativeStrengthIndex(indicator.Indicator):
    lines = ('rsi',)

    def __init__(self, period: int):
        super().__init__()
        self.period = period
        self.uperma_n = 0
        self.downrma_n = 0
        self.prev_value = 0
        self.up_diffs = []
        self.down_diffs = []

    def next(self):
        if len(self.up_diffs) == self.period:
            self.up_diffs.pop(0)
            self.down_diffs.pop(0)

        current_price = self.get_price()
        if current_price >= self.prev_value:
            self.up_diffs.append(current_price-self.prev_value)
            self.down_diffs.append(0)
        else:
            self.up_diffs.append(0)
            self.down_diffs.append(self.prev_value - current_price)
        self.prev_value = current_price

        self.uperma_n = sum(self.up_diffs)/self.period
        self.downrma_n = sum(self.down_diffs)/self.period
        if self.downrma_n ==0:
            self.lines.rsi[0] = 100
            return

        rs = self.uperma_n/self.downrma_n
        self.lines.rsi[0]= 100 - 100/(1 + rs)

    def is_ready(self) -> bool:
        return len(self.up_diffs) == self.period