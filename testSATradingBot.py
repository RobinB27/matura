from datetime import datetime

from TradingBot.Bot import Bot
from TradingBot.SimpleSentimentDM import SimpleSentimentDM


testBot = Bot(SimpleSentimentDM(-1), datetime(2019, 6, 1), -1)
testBot.initialise(10000, ["TSLA"], 40)
testBot.start()
