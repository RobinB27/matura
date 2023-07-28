from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt
from TradingBot.MACDDecisionMaking import MACDDecisionMaking

a = Bot("2023-2-19", -1)
t1 = Stock("TSLA")


a.initiating()
a.startBot()

#fix issue with download after an exception/weekend date in EMA calculations line 63-71
#2023-2-19 is weekend for reference