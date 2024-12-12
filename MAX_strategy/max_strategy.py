from alt_backtest import strategy, position

from MAX_strategy.config import ema_short_period, ema_long_period,start_cash

from MAX_strategy.max_indicators.rsi_indicator import RelativeStrengthIndex
from MAX_strategy.max_indicators.ema_indicator import ExponentialMovingAverage
from MAX_strategy.max_indicators.atr_indicator import AverageTrueRange
from MAX_strategy.max_indicators.stochastic_oscillator import StochasticOscillator
from MAX_strategy.max_indicators.macd_indicator import MovingAverageConvergenceDivergence


class MultiIndicatorStrategy(strategy.Strategy):
    order = None

    def __init__(self):
        super().__init__()
        # Инициализация индикаторов
        self.ema_short = ExponentialMovingAverage(period=ema_short_period)
        self.ema_middle = ExponentialMovingAverage(period=7)
        self.ema_long = ExponentialMovingAverage(period=ema_long_period)
        self.ema = ExponentialMovingAverage(period=7)
        self.rsi = RelativeStrengthIndex(period=12)
        self.atr = AverageTrueRange(period=7)
        self.macd = MovingAverageConvergenceDivergence(long_period=20, short_period=9)
        self.stochastic_long = StochasticOscillator(period=9)
        self.stochastic_short = StochasticOscillator(period=3)

        self.position_status = position.Position.none
        self.order = None

        self.risk_per_trade = 0.05  # Риск на сделку
        self.start_cash = start_cash  # Начальный капитал
        self.entry_price = 0

    def next(self):
        if not all([self.ema.is_ready(), self.rsi.is_ready(), self.atr.is_ready(), self.macd.is_ready(),
                    self.stochastic_long.is_ready()]):
            return

        self.current_price = self.get_price()
        atr_value = self.atr.atr[0]
        position_size = self.calculate_position_size(atr_value)

        if not self.in_position():
            if self.is_flat_market():
                if self.stochastic_short.stoch_osc[0] > 0.8:
                    self.sell_short(position_size)
                    return

            # Восходящий тренд
            if self.macd.macd[0] > self.ema.ema_line[0]:
                if self.stochastic_long.stoch_osc[0] < 0.4 and self.ema_short.ema_line[0] > self.ema_long.ema_line[0] or \
                        self.rsi.rsi[0] < 30:
                    self.buy_long(position_size)
                    return

            # Нисходящий тренд
            if self.macd.macd[0] < self.ema.ema_line[0]:
                if self.stochastic_long.stoch_osc[0] > 0.6 and self.ema_short.ema_line[0] < self.ema_long.ema_line[0] or \
                        self.rsi.rsi[0] > 70:
                    self.sell_short(position_size)
                    return

        # Условия для выхода из позиции
        if self.position_status == position.Position.long:
            if self.stochastic_long.stoch_osc[0] > 0.6 or (self.macd.macd[-1] > self.ema.ema_line[-1] and self.macd.macd[0] < self.ema.ema_line[
                0]) or self.current_profit() > 1 * self.atr.atr[0] or self.rsi.rsi[0] > 70:
                self.close_position("SELL_LONG")
                return

        if self.position_status == position.Position.short:
            if self.stochastic_long.stoch_osc[0] > 0.6 or ( self.macd.macd[-1] < self.ema_middle.ema_line[-1] and self.macd.macd[0] > self.ema_middle.ema_line[
                0]) or self.current_profit() > 1 * self.atr.atr[0] or self.current_profit() < -2 * self.atr.atr[0] or self.rsi.rsi[0] > 70:
                self.close_position("SELL_SHORT")
                return

    def calculate_position_size(self, atr_value):
        """Рассчитывает размер позиции на основе ATR и риска."""
        capital = self.get_current_balance()
        risk_per_trade = capital * self.risk_per_trade
        size = risk_per_trade / atr_value
        return size

    def is_flat_market(self):
        """Определяет, является ли рынок флэтовым."""
        macd_threshold = 1
        return all(abs(self.macd.macd[-i]) < macd_threshold for i in range(5))

    def buy_long(self, position_size):
        """Открыть лонг позицию."""
        self.entry_price = self.current_price
        self.order = self.send_market_order_buy(size=position_size)
        self.position_status = position.Position.long
        #print("BUY LONG")

    def sell_short(self, position_size):
        """Открыть шорт позицию."""
        self.entry_price = self.current_price
        self.order = self.send_market_order_sell(size=position_size)
        print(self.order)
        self.position_status = position.Position.short
        #print("SELL SHORT")

    def close_position(self, reason):
        """Закрыть текущую позицию."""
        if self.position_status == position.Position.long:
            self.send_market_order_sell(size=self.order.size)
        elif self.position_status == position.Position.short:
            self.send_market_order_buy(size=self.order.size)
        self.position_status = position.Position.none
        #print(f"Position closed: {reason}")

    def current_profit(self):
        """Вычисляет текущую прибыль по открытой позиции."""
        if not self.in_position():
            return 0
        if self.position_status == position.Position.long:
            return self.current_price - self.entry_price
        if self.position_status == position.Position.short:
            return self.entry_price - self.current_price
        return 0
