from DataGen.Testing import Testing

from datetime import datetime

from TradingBot.Strategies.MACDDM import MACDDM
from TradingBot.Strategies.SimpleSentimentDM import SimpleSentimentDM
from TradingBot.Strategies.AvgSentimentDM import AvgSentimentDM
from TradingBot.Strategies.BuyAndHoldDM import BuyAndHoldDM

# Rarely crashes because getPrice yields None, also slow: needs optimisation
#Testing.compareDMs(100, SimpleSentimentDM, MACDDM, periodLimits=100, funds=10000)

Testing.compareDMs(500, [AvgSentimentDM, BuyAndHoldDM], 10000, startDate=None, stockList=None, periodLimits=100)