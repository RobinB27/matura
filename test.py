from DataGen.Testing import Testing

from TradingBot.MACDDM import MACDDM
from TradingBot.SimpleSentimentDM import SimpleSentimentDM

# Rarely crashes because getPrice yields None, also slow: needs optimisation
Testing.compareDMs(100, SimpleSentimentDM, MACDDM, periodLimits=100, funds=10000)