from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot

p1 = Portfolio(1000, "first")
s1 = Stock("AAPL")

s1.getStockPrice(-1,'2016-01-04','2016-01-05')