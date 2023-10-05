from DataGen.Testing import Testing

from datetime import datetime

from TradingBot.MACDDM import MACDDM
from TradingBot.SimpleSentimentDM import SimpleSentimentDM

# Rarely crashes because getPrice yields None, also slow: needs optimisation
#Testing.compareDMs(100, SimpleSentimentDM, MACDDM, periodLimits=100, funds=10000)

now = datetime.now()

Testing.compareDMs(400, SimpleSentimentDM, MACDDM, 10000, startDate=None, stockList=None, periodLimits=100)

then = datetime.now()

print(then, now, then - now)     