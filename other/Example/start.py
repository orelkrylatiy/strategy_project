from alt_backtest import start

import config
from config import start_cash,data__path, start_date,end_date, format_date
from sma_strategy import SMAStrategy


print(config.name)
start.run(SMAStrategy, start_cash,data__path,start_date,end_date, format_date)

