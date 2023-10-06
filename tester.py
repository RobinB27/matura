from datetime import datetime
from TradingBot.Stock import Stock

ts = Stock("TSLA")

print(ts.getPrice(-1, datetime(2012, 12, 17)))