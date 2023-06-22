from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.Bot import Bot
import yfinance as yf
from TradingBot.FileLoggertxt import FileLogger
from TradingBot.MACDDecisionMaking import MACDDecisionMaking


p1 = Portfolio(1000, "Test")
p1.addStock("TSLA")

s1 = Stock("TSLA")

#problematic date, i have no idea why
#Debugger information from the date  on the that might help 
#(return)Empty DataFrame
#style: '<pandas.io.formats.style.Styler -- debugger: skipped eval>'

#'<transposed dataframe -- debugger:skipped eval>'
#print(s1.getStockPrice(-1, "2023-05-29", "2023-05-30"))

# 29th June is bank holiday => add fix for holidays 

d1 = MACDDecisionMaking(0)

#on the "2023-05-29" the getStockPrice() function fails, mode=-1, the pandas dataframe is empty
#Error message:
#ERROR ['TSLA']: Exception('TSLA: No price data found, symbol may be delisted (1d 2023-05-29 -> 2023-05-30)')
#SMA_Value +=  stock.getStockPrice(-1, placeHolderDate, secondPlaceHolderDate)
#TypeError: unsupported operand type(s) for +: 'float' and 'NoneType'

print(d1.calculateSMA(12, p1, "TSLA"))
