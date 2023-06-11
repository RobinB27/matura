import yfinance as fy
from datetime import datetime, timedelta, date
import pandas as pd
from TradingBot.Portfolio import Portfolio

class MACDDecisionMaking:
    
    def __init__(self, mode: int = 0, startDate: str = "0"):
        
        self.date = startDate
        
    
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
            
            #doesnt work, because the way the getstockprice function searches for the closing price
            #should output the SMA value for avariable number of days
            for stock in portfolio.stocksHeld:
                    if stock.name == ticker:  
                        SMA_Value +=  stock.getStockPrice()
                        #iterates over the past stock prices and adds the closing stock price to the SMA claculation from the current date backwards
                        for i in range(daysToCalculate):
                            placeHolderDate = startDate - timedelta(days=1)
                            secondPlaceHolderDate = placeHolderDate + timedelta(days=1)
                            
                            placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                            secondPlaceHolderDate = secondPlaceHolderDate.strftime("%Y-%m-%d")
                            
                            SMA_Value +=  stock.getStockPrice(-1, placeHolderDate, secondPlaceHolderDate)
                             
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
        