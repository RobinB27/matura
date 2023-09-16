from datetime import datetime

from TradingBot.Bot import Bot
from TradingBot.AvgSentimentDM import AvgSentimentDM

# Fixed a bug caused by faulty caching
""" ticker = "TSLA"
date = datetime(2020, 6, 1)
dm = AvgSentimentDM(-1)

print(dm.getSMA(date, 12, ticker), dm.getSMA(date, 26, ticker))
print(dm.getEMA(date, 12, ticker), dm.getEMA(date, 26, ticker))
print(dm.getMACD(date, ticker))
print(dm.getSIG(date, ticker)) 
"""

bot = Bot(AvgSentimentDM(-1), datetime(2020, 1, 1), -1)
bot.initialise(1000, ["TSLA"], 50)
bot.start()