import yfinance as yf

from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot

from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt
from TradingBot.MACDDecisionMaking import MACDDecisionMaking

from TradingBot.FinancialCalculators.EMACalculator import EMACalculator
from TradingBot.FinancialCalculators.MACDCalculator import MACDCalculator
from TradingBot.FinancialCalculators.SignalLineCalculator import SignalLineCalculator

#to implement some form of


# Use datetime dates instead of date strings as function, eliminates your problem

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#bot settings need date format like this: "2023-04-12"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
a = Bot(MACDDecisionMaking(-1), "2022-01-04", -1)
t1 = Stock("TSLA")
p = Portfolio(1000)
p.addStock("TSLA")

#stockPrice = t1.getStockPrice(-1, "2020-04-12", "2020-04-13")
#print(stockPrice)

c1 = MACDCalculator() 
s = SignalLineCalculator()
E = EMACalculator()

#print(t1.getStockPrice(-1, "2023-05-29"))
# , "2023-04-19"))

#print(M.calculateSMA(12, p, "TSLA", -1, "2020-05-25"))
#print(E.calculateEMA(12, p, "TSLA", -1, "2023-03-17"))
#print("EMA: 2023-04-18: 186.83")
#print(c1.calculateMACD(p, "TSLA", -1, "2023-08-08"))
#print(s.signalLineCalculation(p, "TSLA", -1, "2022-03-24"))

a.initiating()
a.startBot()
