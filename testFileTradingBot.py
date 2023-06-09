from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot

p1 = Portfolio(1000, "first")


p1.addStock("TSLA")
p1.buyStock(3, "TSLA", -1, "2020-12-31")
print(p1.funds)
p1.sellStock(2, "TSLA", -1, "2020-12-31")
print(p1.funds)
