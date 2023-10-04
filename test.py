from DataGen.Testing import Testing

from datetime import datetime

from TradingBot.MACDDM import MACDDM
from TradingBot.SimpleSentimentDM import SimpleSentimentDM
from TradingBot.BuyAndHoldDM import BuyAndHoldDM

# Rarely crashes because getPrice yields None, also slow: needs optimisation
#Testing.compareDMs(100, SimpleSentimentDM, MACDDM, periodLimits=100, funds=10000)

now = datetime.now()

Testing.compareDMs(2, BuyAndHoldDM, MACDDM, 10000, startDate=None, stockList=None, periodLimits=100)

then = datetime.now()

print(then, now, then - now)