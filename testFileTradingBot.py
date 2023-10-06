from datetime import datetime
from diskcache import Cache


from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.SignalLineCalculator import SignalLineCalculator
from TradingBot.Bot import Bot
from TradingBot.MACDDM import MACDDM


#1h intervals are the highest granularity of data allowed for live mode at present

p = Portfolio(10000)
p.addStock("ADBE")
s = SignalLineCalculator



a = Stock("ADBE")
#a.clearCache()
#print(a.getPricesUntilDate(datetime(2020, 2, 6)))

print(s.signalLineCalculation(s, p, "ADBE", -1, datetime(2020, 2, 6)))