import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.SMACalculator import SMACalculator

class EMACalculator:
    
    def __init__(self) -> None:
        self.SMACAlculator = SMACalculator()
    
    def calculateEMA(self, daysToCalculate: int, portfolio: Portfolio, ticker, mode = 0, dateToCalculate = "0"):
        """Calculates the EMA needed for MACD calculations

        Args:
            daysToCalculate (int): _description_
            portfolio (_type_): _description_
            ticker (_type_): _description_
            mode (int, optional): _description_. Defaults to 0.
            dateToCalculate (str, optional): _description_. Defaults to "0".

        Returns:
            _type_: _description_
        """
        
        #EMA(today) = (Close(today) * α) + (EMA(yesterday) * (1 - α))
        
        weightMultiplier = 2 / (daysToCalculate + 1)
        
        #could be optimised with keeping a running EMA calculation, this recalculates the EMA every time it's called
        if mode == 0:
            
            placeholderWeekendCheck = datetime.strptime(dateToCalculate, "%Y-%m-%d")
            #checks if dateToCalculate is on a weekend()
            if placeholderWeekendCheck.isoweekday() > 5:
                print("EMA calculatins not possible on a weekend")
                exit()
                
            placeHolderExceptionCheck = placeholderWeekendCheck.strftime("%Y-%m-%d")
            # implement exception date check
            
            
            EMAValue = 0
            
            SMA_Placeholder = self.SMACAlculator.calculateSMA(daysToCalculate, portfolio, ticker)
            
            stockPrice = 0
            for stock in portfolio.stocksHeld:
                if stock.name == ticker:
                    stockPrice = stock.getStockPrice()
                    
            EMAValue = (stockPrice * weightMultiplier) + (SMA_Placeholder * (1 - weightMultiplier))
            
            return EMAValue
            
        elif mode == -1:
            
            
            SMA_Placeholder = 0
            
            placeHolderDate = datetime.strptime(dateToCalculate, "%Y-%m-%d")
            getStockPricePlacholder = placeHolderDate
            
            getStockPricePlacholder += timedelta(1)
            getStockPricePlacholder = getStockPricePlacholder.strftime("%Y-%m-%d")
            
            for stock in portfolio.stocksHeld:
                if stock.name == ticker:
                    SMA_Placeholder += self.SMACAlculator.calculateSMA(daysToCalculate, portfolio, ticker, -1,  dateToCalculate)

                        
            stockPrice = 0
            stockPrice = stock.getStockPrice(-1, dateToCalculate, getStockPricePlacholder)
                    
            EMAValue = (stockPrice * weightMultiplier) + (SMA_Placeholder * (1 - weightMultiplier))
           
            return EMAValue
