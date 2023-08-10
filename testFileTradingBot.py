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
a = Bot(MACDDecisionMaking(-1), "2020-03-15", -1)
t1 = Stock("TSLA")
p = Portfolio(1000)
p.addStock("TSLA")

#stockPrice = t1.getStockPrice(-1, "2020-04-12", "2020-04-13")
#print(stockPrice)

c1 = MACDCalculator() 
s = SignalLineCalculator()
M = SMACalculator()
E = EMACalculator()

#print(t1.getStockPrice(-1, "2023-04-18"
# , "2023-04-19"))

#print(M.calculateSMA(12, p, "TSLA", -1, "2023-04-18"))
#print(E.calculateEMA(12, p, "TSLA", -1, "2023-04-18"))
#print(c1.calculateMACD(p, "TSLA", -1, "2023-04-18"))
#print(s.signalLineCalculation(p, "TSLA", -1, "2023-04-18"))

a.initiating()
a.startBot()

#bot trade for 12 days on 2023-04-24 and then 27 should be a signal but bot does not identify it

#8. 1h bugfixes
#9. 3h 15min bugfixes

