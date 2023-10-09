from datetime import datetime
from diskcache import Cache
import yfinance as yf


from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.SignalLineCalculator import SignalLineCalculator
from TradingBot.Bot import Bot
from TradingBot.MACDDM import MACDDM


#1h intervals are the highest granularity of data allowed for live mode at present

p= Portfolio(1000)
p.addStock("TSLA")
sig = SignalLineCalculator()

line = sig.signalLineCalculation(p, "TSLA", 0, datetime(2023, 8, 10), 2)

print(line)