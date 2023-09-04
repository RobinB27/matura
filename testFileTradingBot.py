from datetime import datetime

from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
from TradingBot.MACDDM import MACDDM

#to implement some form of


# Use datetime dates instead of date strings as function, eliminates your problem

#1h intervals are the highest granularity of data allowed for live mode at present

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#bot settings need date format like this: "2023-04-13"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#a = Bot(MACDDecisionMaking(-1), "2022-01-07", -1)
a = Bot(MACDDM(-1), datetime(2022, 8, 1), -1)
t1 = Stock("TSLA")
p = Portfolio(1000)
p.addStock("TSLA")

#stockPrice = t1.getStockPrice(-1, "2020-04-12", "2020-04-13")
#stockPrice = t1.getPrice()
#print(stockPrice)


#print(stockPrice)

#s = SignalLineCalculator()


#print(t1.getStockPrice(-1, "2023-05-29"))
# , "2023-04-19"))

#print(s.signalLineCalculation(p, "TSLA", -1, "2022-05-22"))

a.initialise(1000, ["TSLA"], 40)
a.start()
