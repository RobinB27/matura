import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.EMACalculator import EMACalculator

from Util.Config import Config


class MACDCalculator:
    
    def __init__(self):
        self.EMACalculator = EMACalculator()
    
    def calculateMACD(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateStart: str = "0"):
        
        # MACD = 12 day EMA - 26 day EMA
        # EMA = exponential moving average
        
        # thought that maybe two modes arent needed because the code in mode = 0 should work for every date given (needs testing)
        # the above thought isnt possible due to the way the getStockPrice() function is implemented
        
        # mode is currently using the function param mode, couldn't this be the class variable?
        
        if mode == 0:
            
            if Config.debug():  
                print(f"MACDCalculator: Downloading EMA 12")
            EMA_Placeholder12days = self.EMACalculator.calculateEMA(12, portfolio, ticker)
            if Config.debug():  
                print(f"MACDCalculator: Downloading EMA 26")
            EMA_Placeholder26days = self.EMACalculator.calculateEMA(26, portfolio, ticker)

            MACDline = EMA_Placeholder12days - EMA_Placeholder26days
            return MACDline
            
            
            
        elif mode == -1:
            
            
            if Config.debug():  
                print(f"MACDCalculator: Downloading EMA 12: {dateStart}")
            EMA_Placeholder12days = self.EMACalculator.calculateEMA(12, portfolio, ticker, -1, dateStart)
            
            if Config.debug():  
                print(f"MACDCalculator: Downloading EMA 26: {dateStart}")
            EMA_Placeholder26days = self.EMACalculator.calculateEMA(26, portfolio, ticker, -1, dateStart)
            

            
            MACDline = EMA_Placeholder12days - EMA_Placeholder26days
            return round(MACDline, 2)
