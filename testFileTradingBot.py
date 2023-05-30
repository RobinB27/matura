from TradingBot.Portfolio import Portfolio
from TradingBot.Stock import Stock

p1 = Portfolio(1000)

p1.addStock("TSLA")
p1.buyStock(2, "TSLA")
print(p1.funds)
print(p1.stocksHeld.get["0"])