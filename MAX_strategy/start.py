from alt_backtest import start

from other import config
from other.config import start_cash,data__path, start_date,end_date, format_date
#from max_strategy import TrendStrategy
from max_strategy import MultiIndicatorStrategy


print(config.name)

start.run(MultiIndicatorStrategy, start_cash,data__path,start_date,end_date, format_date)
