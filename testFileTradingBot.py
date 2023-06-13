from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLoggertxt import FileLogger
from TradingBot.MACDDecisionMaking import MACDDecisionMaking


p1 = Portfolio(1000, "Test")
p1.addStock("TSLA")

s1 = Stock("TSLA")
print(s1.getStockPrice(-1, "2023-05-29", "2023-05-30"))

d1 = MACDDecisionMaking(0)

#print(d1.calculateSMA(12, p1, "TSLA"))
