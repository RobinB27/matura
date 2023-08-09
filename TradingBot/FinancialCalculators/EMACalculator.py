import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.SMACalculator import SMACalculator

from diskcache import Cache

from Util.Config import Config


class EMACalculator:
    
    def __init__(self) -> None:
        self.SMACAlculator = SMACalculator()
        self.cache = Cache("./TradingBot/FinancialCalculators/CacheSMA")

    
    def calculateEMA(self, daysToCalculate: int, portfolio: Portfolio, ticker, mode = 0, dateToCalculate:str = ""):
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
        
        #mode 0 needs biiig rework
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
            Stock_Price_Value = self.SMACAlculator.calculateSMA(daysToCalculate, portfolio, ticker)
            EMAValue = (stockPrice * weightMultiplier) + (Stock_Price_Value * (1 - weightMultiplier))
            
            return EMAValue
            
        elif mode == -1:
            
            #EMA(today) = (Close(today) * α) + (EMA(yesterday) * (1 - α))
            
            #checks if date is a weekend, meaning no price
            
            Stock_Price_Value = []
            Stock_Price_Value.append(self.SMACAlculator.calculateSMA(daysToCalculate, portfolio, ticker, -1,  dateToCalculate))

            executions = 0
            
            while executions < daysToCalculate - 1:
                placeHolderDate = datetime.strptime(dateToCalculate, "%Y-%m-%d")
                if placeHolderDate.isoweekday() > 5:
                    dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                    continue
                            
                #checks if dateToCalculate is an exception date for stock market closure
                getStockPricePlacholder = portfolio.addDayToDate(dateToCalculate)
                            
                #key for cache
                key = ticker + "_" + dateToCalculate
                            
                if key not in self.cache:
                    self.cache[key] = stock.getStockPrice(-1, dateToCalculate, getStockPricePlacholder)
                if self.cache[key] == None:
                    if Config.debug():
                        print("EMACalculator: Exception check cache")
                    dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                    continue
                elif self.cache[key] == None:
                    if Config.debug():
                        print("EMACalculator: Exception check cache access")
                    dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                    continue             
                        
                if Config.debug():  
                    print(f"EMACalculator: Downloading SMA values on: {dateToCalculate}") 
                      
                #Stock_Price_Value.append(self.SMACAlculator.calculateSMA(daysToCalculate, portfolio, ticker, -1,  dateToCalculate))
                for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        
                        Stock_Price_Value.append(stock.getStockPrice(-1, dateToCalculate))

                dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)

                executions += 1
                
            #EMA(today) = (Close(today) * α) + (EMA(yesterday) * (1 - α))
                
            EMA_Value = Stock_Price_Value[0]
            
            for i in range(1, len(Stock_Price_Value)):
                #EMA_Value = (Stock_Price_Value[i] * weightMultiplier) - (EMA_Value * (1 - weightMultiplier))
                #EMA(today) = (Close(today) * α) + (EMA(yesterday) * (1 - α))

                EMA_Value = (((Stock_Price_Value[i] - (EMA_Value)) * weightMultiplier) + EMA_Value)
                   
            return EMA_Value