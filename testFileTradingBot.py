from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLogger import FileLogger


p1 = Portfolio(1000, "first")
p1.addStock("TSLA")
p1.addStock("AAPL")
a = FileLogger("test")

a.snapshot(p1, "2022-12-2")
