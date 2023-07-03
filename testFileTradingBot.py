from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLoggertxt import FileLogger
from TradingBot.MACDDecisionMaking import MACDDecisionMaking


p1 = Portfolio(1000, "Test")
p1.addStock("AAPL")

s1 = Stock("TSLA")

d1 = MACDDecisionMaking(0)

print(d1.makeStockDecision(p1, "1", -1, "2023-1-13"))
