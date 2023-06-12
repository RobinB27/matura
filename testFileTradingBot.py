from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLogger import FileLogger
from TradingBot.MACDDecisionMaking import MACDDecisionMaking


p1 = Portfolio(1000, "Test")
p1.addStock("TSLA")



s1 = Stock("TSLA")

d1 = MACDDecisionMaking(0)

print(d1.calculateSMA(12, p1, "TSLA"))
