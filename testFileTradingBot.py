from datetime import datetime
from diskcache import Cache


from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
from TradingBot.MACDDM import MACDDM


#1h intervals are the highest granularity of data allowed for live mode at present

a = Stock("ADBE")

runNumber = 0

while True:
    price = a.getPricesUntilDate(datetime(2019, 10, 31))
    
    if price is None or price == 0 or len(price) == 0:
        print("error in price getting")
        break
    print(runNumber)
    runNumber += 1