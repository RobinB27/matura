from datetime import datetime
from diskcache import Cache
import yfinance as yf


from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.SignalLineCalculator import SignalLineCalculator
from TradingBot.Bot import Bot
from TradingBot.MACDDM import MACDDM


#1h intervals are the highest granularity of data allowed for live mode at present

stock = yf.Ticker("TSLA")
print(stock.info)

tesla = Stock("TSLA")
print(tesla.getPrice(0))