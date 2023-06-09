import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.EMACalculator import EMACalculator

class MACDCalculator:
    
    def __init__(self) -> None:
        self.EMACalculator = EMACalculator()
    
    def calculateMACD(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateStart: str = "0"):
        
        # MACD = 12 day EMA - 26 day EMA
        # EMA = exponential moving average
        
        # thought that maybe two modes arent needed because the code in mode = 0 should work for every date given (needs testing)
        # the above thought isnt possible due to the way the getStockPrice() function is implemented
        
        # mode is currently using the function param mode, shouldn't this be the class variable?
        
        if mode == 0:
            
            EMA_Placeholder12days = self.EMACalculator.calculateEMA(12, portfolio, ticker)
            EMA_Placeholder26days = self.EMACalculator.calculateEMA(26, portfolio, ticker)

            MACDline = EMA_Placeholder12days - EMA_Placeholder26days
            return MACDline
            
            
            
        elif mode == -1:
            
            
            
            EMA_Placeholder12days = self.EMACalculator.calculateEMA(12, portfolio, ticker, -1, dateStart)
            EMA_Placeholder26days = self.EMACalculator.calculateEMA(26, portfolio, ticker, -1, dateStart)

            
            MACDline = EMA_Placeholder12days - EMA_Placeholder26days
            return MACDline
