from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt
from TradingBot.MACDDecisionMaking import MACDDecisionMaking

from TradingBot.FinancialCalculators.SMACalculator import SMACalculator
from TradingBot.FinancialCalculators.EMACalculator import EMACalculator
from TradingBot.FinancialCalculators.MACDCalculator import MACDCalculator
from TradingBot.FinancialCalculators.SignalLineCalculator import SignalLineCalculator




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#bot settings need date format like this: "2023-04-12"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
a = Bot(MACDDecisionMaking(-1), "2023-03-15", -1)
t1 = Stock("TSLA")
p = Portfolio(1000)
p.addStock("TSLA")

#stockPrice = t1.getStockPrice(-1, "2020-04-12", "2020-04-13")
#print(stockPrice)

c1 = MACDCalculator() 
s = SignalLineCalculator()
M = SMACalculator()

print(t1.getStockPrice(-1, "2020-04-14", "2020-04-15"))

print(M.calculateSMA(12, p, "TSLA", -1, "2020-04-13"))
#print(c1.calculateMACD(p, "TSLA", -1, "2020-04-14"))
#print(s.signalLineCalculation(p, "TSLA", -1, "2020-04-14"))

a.initiating()
a.startBot()
