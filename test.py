from DataGen.Testing import Testing

from datetime import datetime

from TradingBot.MACDDM import MACDDM
from TradingBot.SimpleSentimentDM import SimpleSentimentDM

# Rarely crashes because getPrice yields None, also slow: needs optimisation
#Testing.compareDMs(100, SimpleSentimentDM, MACDDM, periodLimits=100, funds=10000)

Testing.testTimeFrame(SimpleSentimentDM, 1000, datetime(2011, 1, 1), datetime(2020, 6, 11))