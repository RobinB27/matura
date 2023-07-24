import yfinance as fy
import pandas as pd
import diskcache

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio
    
    #lot of boilerplate can be removed by putting the while loop inside it's own function

class SMACalculator:
    
    def __init__(self):
        #creates cache for storing SMA values
        cache = diskcache.Cache("./TradingBot/FinancialCalculators/CacheSMA")
    
    def calculateSMA(self, daysToCalculate: int, portfolio: Portfolio, ticker, mode = 0, dateToCalculate = ""):
        """calculates the SMA of a stock, variable time period, mode 0 for current time, mode -1 for past prices

        Args:
            daysToCalculate (int): _description_ 
            portfolio (_type_): _description_
            ticker (_type_): _description_
            mode (int, optional): _description_. Defaults to 0.
            dateToCalculate (str, optional): _description_. Defaults to "0".

        Returns:
            _type_: _description_
        """
        
        SMA_Value = 0
        
        if mode == 0:
            startDate = date.today()
            #checks if the called date is a weekend or a holiday
            if startDate.isoweekday()  > 5:
                print("It's the weekend no current stock prices available to buy")
                exit()
            
            for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        #checks if the stockmarket is open yet
                        if stock.getStockPrice() is None:
                            exit()
                        #adds the current price to the SMA_Value  
                        else:   
                            SMA_Value +=  stock.getStockPrice()
                            placeHolderDate = startDate.strftime("%Y-%m-%d")
                            
                        #iterates over the past stock prices and adds the closing stock price to the SMA claculation from the current date backwards 
                        while executions < daysToCalculate - 1:
                                                                         
                            #checks if date is a weekend, meaning no price
                            weekendCheckPlaceholder = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                            
                            if weekendCheckPlaceholder.isoweekday() > 5:
                                print(f"weekend: {placeHolderDate}")
                                placeHolderDate = portfolio.subtractDayFromDate(placeHolderDate)
                                continue
                            
                            #checks if dateToCalculate is an exception date for stock market closure
                            getStockPricePlacholder = portfolio.addDayToDate(placeHolderDate)
                            
                            if stock.getStockPrice(-1, placeHolderDate, getStockPricePlacholder) is None:
                                placeHolderDate = portfolio.subtractDayFromDate(placeHolderDate)
                                continue                          
                                
                            SMA_Value +=  stock.getStockPrice(-1, placeHolderDate, getStockPricePlacholder)
                            
                            #ensures that a new date is processed in the next iteration
                            placeHolderDate = portfolio.subtractDayFromDate(placeHolderDate)                                
                            executions += 1
                                                  
                        #divides the total value by number of days to get the SMA
                        SMA_Value = SMA_Value / daysToCalculate
                        return SMA_Value
                
        elif mode == -1:
            
            for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        
                        executions = 0
                        while executions < daysToCalculate:
                            
                            #checks if date is a weekend, meaning no price
                            placeHolderDate = datetime.strptime(dateToCalculate, "%Y-%m-%d")

                            if placeHolderDate.isoweekday() > 5:
                                print(f"weekend: {dateToCalculate}")
                                dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                                continue
                            
                            #checks if dateToCalculate is an exception date for stock market closure
                            getStockPricePlacholder = portfolio.addDayToDate(dateToCalculate)
                            
                            if stock.getStockPrice(-1, dateToCalculate, getStockPricePlacholder) is None:
                                dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                                continue                          
                                
                            SMA_Value +=  stock.getStockPrice(-1, placeHolderDate, getStockPricePlacholder)
                            
                            #ensures that a new date is processed in the next iteration
                            dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)                                
                            executions += 1
                          
                        #divides the total value by number of days to get the SMA
                        SMA_Value = SMA_Value / daysToCalculate
                        return SMA_Value