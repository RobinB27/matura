from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf

p1 = Portfolio(1000, "GOAT")
p1.addStock("AAPL")

p1.buyStock(1, "AAPL", -1, "2020-12-3")
p1.sellStock(1, "AAPL", -1, "2020-12-3")