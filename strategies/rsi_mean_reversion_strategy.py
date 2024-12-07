class RelativeStrengthIndex(indicator.Indicator):
    lines = ('rsi',)

    def __init__(self, period: int):
        super().__init__()
        self.period = period
        self.gains = []
        self.losses = []

    def next(self):
        price = self.get_price()
        if not hasattr(self, 'prev_price'):
            self.prev_price = price
            return

        change = price - self.prev_price
        self.prev_price = price

        if change > 0:
            self.gains.append(change)
            self.losses.append(0)
        else:
            self.gains.append(0)
            self.losses.append(abs(change))

        if len(self.gains) > self.period:
            self.gains.pop(0)
            self.losses.pop(0)

        avg_gain = sum(self.gains) / self.period if len(self.gains) == self.period else 0
        avg_loss = sum(self.losses) / self.period if len(self.losses) == self.period else 0

        if avg_loss == 0:
            self.lines.rsi[0] = 100
        else:
            rs = avg_gain / avg_loss
            self.lines.rsi[0] = 100 - (100 / (1 + rs))

    def is_ready(self) -> bool:
        return len(self.gains) == self.period
