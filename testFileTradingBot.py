from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt
from TradingBot.MACDDecisionMaking import MACDDecisionMaking

a = Bot("2023-4-12", -1)
t1 = Stock("TSLA")

#t1.getStockPrice(-1, "2023-2-20", "2023-2-21")


a.initiating()
a.startBot()

#checks for weekend/exception date in crossings checks in decisionmaking

