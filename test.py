import numpy as np
import yfinance as yf

from TradingBot.Stock import Stock


a = Stock("TSLA")

b = a.getPrice()
print(b)