from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLoggertxt import FileLoggertxt
from TradingBot.MACDDecisionMaking import MACDDecisionMaking

a = Bot("0", -1)

a.initiating()
a.startBot()