import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio 
    
    #lot of boilerplate can be removed by putting the while loop inside it's own function

class SMACalculator:
    
    def calculateSMA(self, daysToCalculate: int, portfolio: Portfolio, ticker, mode = 0, dateToCalculate = "0"):
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
            
        
            #should output the SMA value for avariable number of days
            for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        #checks if the stockmarket is open yet
                        #this has the potential to get buggy/confusing if the day is a holiday since it will never open
                        if stock.getStockPrice() is None:
                            print("no stock price available yet")
                            exit()
                        #adds the current price to the SMA_Value  
                        else:   
                            SMA_Value +=  stock.getStockPrice()
                            placeHolderDate = startDate - timedelta(days=1)
                        #iterates over the past stock prices and adds the closing stock price to the SMA claculation from the current date backwards 
                        
                        
                        executions = 0
                        while executions != daysToCalculate - 1:
                            
                            #checks if date is a weekend, meaning no price
                            if placeHolderDate.isoweekday() > 5:
                                placeHolderDate -= timedelta(days=1)
                                print(f"Weekend on: {placeHolderDate}")
                                continue
                            if stock.getStockPrice(-1, placeHolderDate) is None:
                                placeHolderDate -= timedelta(days=1)
                                print("exception date")
                                continue
                                
                            else:
                                
                                secondplaceHolderDate = placeHolderDate + timedelta(days=1)
                            
                                #converts the datetime objects into str format for getStockPrice()
                                placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                                secondplaceHolderDate = secondplaceHolderDate.strftime("%Y-%m-%d")
                                
                                #check if the stockmarket is open on that day (holiday check)
                                if stock.getStockPrice(-1, placeHolderDate, secondplaceHolderDate) is None:
                                    placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                                    placeHolderDate -= timedelta(days=1)
                                    continue
                                
                                SMA_Value +=  stock.getStockPrice(-1, placeHolderDate, secondplaceHolderDate)
                                
                                #converts the str back into datetime objects
                                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                                secondplaceHolderDate = datetime.strptime(secondplaceHolderDate, "%Y-%m-%d") #not sure if line is needed, to test
                                
                                placeHolderDate -= timedelta(days=1)
                            executions += 1
                          
                        #divides the total value by number of days to get the SMA
                        SMA_Value = SMA_Value / daysToCalculate
                        return SMA_Value
                
        elif mode == -1:
            
            for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        
                        executions = 0
                        placeHolderDate = datetime.strptime(dateToCalculate, "%Y-%m-%d")
                        
                        while executions < daysToCalculate:
                            
                            #checks if date is a weekend, meaning no price
                            #DOESNT WORK
                            if placeHolderDate.isoweekday() > 5:
                                placeHolderDate -= timedelta(days=1)
                                continue
                            
                            #creates the second date needed for the getStockPrice function
                            getStockPricePlacholder = placeHolderDate
                            getStockPricePlacholder += timedelta(days=1)
                            
                            
                            placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                            getStockPricePlacholder = getStockPricePlacholder.strftime("%Y-%m-%d")
                            
                            if stock.getStockPrice(-1, placeHolderDate, getStockPricePlacholder) is None:
                                
                                placeHolderDate =  datetime.strptime(placeHolderDate, "%Y-%m-%d")
                                placeHolderDate -= timedelta(days=1)
                                print("exception date")
                                continue
                            
                            placeHolderDate =  datetime.strptime(placeHolderDate, "%Y-%m-%d")   
                        
                            secondplaceHolderDate = placeHolderDate + timedelta(days=1)
                            
                            #converts the datetime objects into str format for getStockPrice()
                            placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                            secondplaceHolderDate = secondplaceHolderDate.strftime("%Y-%m-%d")
                                
                            #check if the stockmarket is open on that day (holiday check)
                            if stock.getStockPrice(-1, placeHolderDate, secondplaceHolderDate) is None:
                                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                                placeHolderDate -= timedelta(days=1) 
                                continue
                                
                            SMA_Value +=  stock.getStockPrice(-1, placeHolderDate, secondplaceHolderDate)
                                
                            #converts the str back into datetime objects
                            placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                            secondplaceHolderDate = datetime.strptime(secondplaceHolderDate, "%Y-%m-%d") #not sure if line is needed, to test
                                
                            placeHolderDate -= timedelta(days=1)
                            executions += 1
                          
                        #divides the total value by number of days to get the SMA
                        SMA_Value = SMA_Value / daysToCalculate
                        return SMA_Value
