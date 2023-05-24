from TradingBot.Portfolio import Portfolio
from TradingBot.Stock import Stock

stock1 = Stock("TSLA")

price = stock1.getCurrentStockPrice()

print(price)

stock1.increaseStockAmount(12)
print(stock1.amountOfStock)
stock1.decreaseStockAmount(34)
print(stock1.amountOfStock)
