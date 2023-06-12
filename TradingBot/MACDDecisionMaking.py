import yfinance as fy
from datetime import datetime, timedelta, date
import pandas as pd
from TradingBot.Portfolio import Portfolio

class MACDDecisionMaking:
    
    
    def __init__(self, mode: int = 0, startDate: str = "0"):
        
        self.date = startDate
        self.mode = mode
        
    
    def makeStockDecision(self, portfolio, stock):
        decision = 0
        return decision
    
    def calculateMACD(self, portfolio, ticker: str, mode: int = 0, dateStart: str = "0"):
        
        #MACD = 12 day EMA - 26 day EMA
        #EMA = exponential moving average
        # simple moving average * (2/days of SMA + 1)
        
        #thought that maybe two modes arent needed because the code in mode = 0 should work for every date given (needs tasting)
        #the above thought isnt possible due to the way the getStockPrice() function is implemented
        
        if mode == 0:
            EMA_Placeholder12days = self.calculateEMA(12, portfolio, ticker)
            EMA_Placeholder26days = self.calculateEMA(26, portfolio, ticker)
            
            MACDline = EMA_Placeholder12days - EMA_Placeholder26days
            
            
            
        elif mode == -1:
            EMAplaceholder = self.calculateEMA(portfolio, ticker, dateStart)
     
        
    def calculateSMA(self, daysToCalculate: int, portfolio, ticker, mode = 0, dateToCalculate = "0"):
        
        SMA_Value = 0
        
        if mode == 0:
            startDate = date.today()
            #checks if the called date is a weekend
            if startDate.isoweekday()  > 5:
                print("It's the weekend no current stock prices available to buy")
                exit()
        
            #should output the SMA value for avariable number of days
            for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        #checks if the stockmarket is open yet
                        if stock.getStockPrice() is None:
                            print("no stock price available yet")
                            exit()
                        #adds the current price to the SMA_Value  
                        else:   
                            SMA_Value +=  stock.getStockPrice()
                            placeHolderDate = startDate - timedelta(days=1)
                        #iterates over the past stock prices and adds the closing stock price to the SMA claculation from the current date backwards 
                        print(SMA_Value)
                        
                        #checks if date is a weekend, meaning no price
                        executions = 0
                        while executions != daysToCalculate - 1:
        
                            if placeHolderDate.isoweekday() > 5:
                                placeHolderDate -= timedelta(days=1)
                                continue
                            else:
                                
                                secondPlaceHolderDate = placeHolderDate + timedelta(days=1)
                            
                                #converts the datetime objects into str format for getStockPrice()
                                placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                                secondPlaceHolderDate = secondPlaceHolderDate.strftime("%Y-%m-%d")
                                
                            
                                SMA_Value +=  stock.getStockPrice(-1, placeHolderDate, secondPlaceHolderDate)
                                
                                #converts the str back into datetime objects
                                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                                secondPlaceHolderDate = datetime.strptime(secondPlaceHolderDate, "%Y-%m-%d")
                                
                                placeHolderDate -= timedelta(days=1)
                            executions += 1
                            print(SMA_Value)
                            print(executions)
                          
                        #divides the total value by number of days to get the SMA
                        SMA_Value = SMA_Value / daysToCalculate
                        return SMA_Value
                
        elif mode == -1:
            pass
                        
                        
    def calculateEMA(self, daysToCalculate: int, portfolio, ticker, mode = 0, dateToCalculate = "0"):
        if mode == 0:
            SMA_Placeholder = self.calculateSMA(daysToCalculate, portfolio, ticker)
        
        elif mode == -1:
            SMA_Placeholder = self.calculateSMA(daysToCalculate, portfolio, ticker, -1,  dateToCalculate)
        