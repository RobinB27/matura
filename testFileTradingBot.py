from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt
from TradingBot.MACDDecisionMaking import MACDDecisionMaking

#bot settings need date format like this: "2023-04-12"
a = Bot(MACDDecisionMaking(-1), "2023-04-12", -1)
t1 = Stock("TSLA")

a.initiating()
a.startBot()

#implement caching for other exception dates checks