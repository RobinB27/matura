from DataGen.Testing import Testing

from datetime import datetime

from TradingBot.MACDDM import MACDDM
from TradingBot.SimpleSentimentDM import SimpleSentimentDM
from TradingBot.AvgSentimentDM import AvgSentimentDM
from TradingBot.BuyAndHoldDM import BuyAndHoldDM

# Rarely crashes because getPrice yields None, also slow: needs optimisation
#Testing.compareDMs(100, SimpleSentimentDM, MACDDM, periodLimits=100, funds=10000)

Testing.compareDMs(50, [AvgSentimentDM, MACDDM], 10000, startDate=None, stockList=None, periodLimits=100)