from alt_backtest import indicator, Price

class StochasticOscillator(indicator.Indicator):
    lines = ('stoch_osc',)

    def __init__(self, period: int):
        super().__init__()
        self.period = period
        self.price_values = []

    def next(self):
        current_price = self.get_price(Price.close)
        self.price_values.append(current_price)

        if len(self.price_values) > self.period:
            self.price_values.pop(0)

            self.lines.stoch_osc[0] = (current_price - min(self.price_values)) / (max(self.price_values) - min(self.price_values))


    def is_ready(self) -> bool:
        return len(self.price_values) == self.period
