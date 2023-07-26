import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.SMACalculator import SMACalculator

class EMACalculator:
    
    def __init__(self) -> None:
        self.SMACAlculator = SMACalculator()
    
    def calculateEMA(self, daysToCalculate: int, portfolio: Portfolio, ticker, mode = 0, dateToCalculate = ""):
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
        EMAValue = 0            
        weightMultiplier = 2 / (daysToCalculate + 1)
        
        #could be optimised with keeping a running EMA calculation, this recalculates the EMA every time it's called
        if mode == 0:
            
            stockPrice = 0
            
            startDate = date.today()
            #checks if dateToCalculate is on a weekend()
            if startDate.isoweekday() > 5:
                print("EMACalculator: EMA calculatins not possible on a weekend")
                exit()
                
            #checks if dateToCalculate is an exception date for stock market closure
            for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        if stock.getStockPrice() is None:
                            print(f"EMACalculator: Market not open/Exception date: {str(startDate)}")
                            exit()
                        else:
                            stockPrice = stock.getStockPrice()
                            
            print("EMACalculator: Downloading SMA values")                         
            SMA_Placeholder = self.SMACAlculator.calculateSMA(daysToCalculate, portfolio, ticker)
            EMAValue = (stockPrice * weightMultiplier) + (SMA_Placeholder * (1 - weightMultiplier))
            
            return EMAValue
            
        elif mode == -1:
                       
            SMA_Placeholder = 0
            stockPrice = 0
            
            getStockPricePlacholder = portfolio.addDayToDate(dateToCalculate)
            
            print(f"EMACalculator: Downloading SMA values on: {dateToCalculate}")                         
            SMA_Placeholder += self.SMACAlculator.calculateSMA(daysToCalculate, portfolio, ticker, -1,  dateToCalculate)
            stockPrice = stock.getStockPrice(-1, dateToCalculate, getStockPricePlacholder)
                    
            EMAValue = (stockPrice * weightMultiplier) + (SMA_Placeholder * (1 - weightMultiplier))
           
            return EMAValue