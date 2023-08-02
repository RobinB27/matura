from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt
from TradingBot.MACDDecisionMaking import MACDDecisionMaking

a = Bot("2023-2-21", -1)
t1 = Stock("TSLA")

#t1.getStockPrice(-1, "2023-2-20", "2023-2-21")


a.initiating()
a.startBot()

#logger needs to deduct initial amount of funds from the log -> self.startingFunds? 

#need to implement that the bot only buy/sells stocks if the line crosses 

#need to check logs if they work