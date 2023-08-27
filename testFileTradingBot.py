import yfinance as yf

from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot

from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt
from TradingBot.MACDDecisionMaking import MACDDecisionMaking
from TradingBot.SimpleSentimentDM import SimpleSentimentDM

from TradingBot.FinancialCalculators.SignalLineCalculator import SignalLineCalculator

#to implement some form of


# Use datetime dates instead of date strings as function, eliminates your problem

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#bot settings need date format like this: "2023-04-13"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
a = Bot(MACDDecisionMaking(0), "2022-01-07", -1)
t1 = Stock("TSLA")
p = Portfolio(1000)
p.addStock("TSLA")

#stockPrice = t1.getStockPrice(-1, "2020-04-12", "2020-04-13")
#print(stockPrice)

s = SignalLineCalculator()


#print(t1.getStockPrice(-1, "2023-05-29"))
# , "2023-04-19"))

#print(s.signalLineCalculation(p, "TSLA", -1, "2022-05-22"))

a.initialiseCLI()
a.start()
