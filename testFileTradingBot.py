from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLogger import FileLogger


p1 = Portfolio(10000, "ToniTest")
logger = FileLogger("Test")

p1.addStock("AAPL")
p1.addStock("TSLA")
p1.buyStock(2, "TSLA")

logger.snapshot(p1)


