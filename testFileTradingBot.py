from TradingBot.Portfolio import Portfolio
from TradingBot.Stock import Stock

p1 = Portfolio(1000, "first")

p1.addStock("TSLA")
p1.showStocksHeld()
p1.showFundsAvailable()
p1.buyStock(3, "TSLA")
p1.showFundsAvailable()
p1.sellStock(2, "TSLA")
p1.showFundsAvailable()