import yfinance as fy
import pandas as pd
import numpy as np
import talib

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.MACDCalculator import MACDCalculator
from diskcache import Cache

from Util.Config import Config


class SignalLineCalculator:
    
    def __init__(self) -> None:
        self.MACDCalculator = MACDCalculator()
        self.cacheExceptionDates = Cache("./TradingBot/FinancialCalculators/Chaches/cacheExceptionDates")
        self.cacheMACD = Cache("./TradingBot/FinancialCalculators/Caches/CacheMACD")

    
    def signalLineCalculation(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateToCalculate: str = ""):
                
        signalLine = 0
        weightMultiplier = 2 / (9 + 1)
        MACDPlaceholder = 0
        
        if mode == 0:
            placeHolderDate = date.today()
            if placeHolderDate.isoweekday() > 5:
                print(f"SignalLineCalculator: live calculations not possible on weekend")
                exit()
            
            for stock in portfolio.stocksHeld():
                if stock.name == ticker & stock.getStockPrice() == None:
                    print("SignalLineCalculator: stock market closed (exception date/closing times)")
                    exit()
                    
            MACDPlaceholder = self.MACDCalculator.calculateMACD(portfolio, ticker)
            print(f"MACD: {MACDPlaceholder} on {str(placeHolderDate)}")
            
            MACDAverage = 0
            executions = 0
            
            #subtracting one day from the start for the EMA calculations of the MACD 
            placeHolderDate = placeHolderDate - timedelta(days=1)
            
            while executions < 9:
                if placeHolderDate.isoweekday() > 5:
                    print(f"SignalLineCalculator while loop 0: Weekend: {str(placeHolderDate)}")
                    placeHolderDate = placeHolderDate - timedelta(days=1)
                    continue
                
                placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                getStockPricePlacholderDate = portfolio.addDayToDate(placeHolderDate)
                
                for stock in portfolio.stocksHeld():
                    if stock.name == ticker & stock.getStockPrice(-1, placeHolderDate, getStockPricePlacholderDate) == None:
                        print(f"SignalLineCalculator while loop 0: stock market closed: {str(placeHolderDate)}")
                        placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                        placeHolderDate = placeHolderDate - timedelta(days=1)
                        continue
                
                MACDAverage += self.MACDCalculator.calculateMACD(portfolio, ticker, -1, placeHolderDate)
                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                executions += 1
            
            MACDAverage = MACDAverage / 9

            signalLine = (MACDPlaceholder * weightMultiplier) + (MACDAverage * (1 - weightMultiplier))
            print(f"SIgnal line: {signalLine}")
            
        elif mode == -1:    
                        
            MACD_prices = []
            
            nextDay = portfolio.addDayToDate(dateToCalculate)
            MACDNextDay = self.MACDCalculator.calculateMACD(portfolio, ticker, -1, nextDay)
            MACD_prices.append(MACDNextDay)
            
            executions = 0
            while executions < 8:
                
                weekendCheck = datetime.strptime(dateToCalculate, "%Y-%m-%d")
                
                if weekendCheck.isoweekday() > 5:
                    if Config.debug():  
                        print(f"SignalLineCalculator while loop -1: Weekend: {dateToCalculate}")
                    dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                    continue
                
                #key for cache
                key = ticker + "_" + dateToCalculate
                
                skipIteration = False
                
                for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        if key not in self.cacheExceptionDates:
                            self.cacheExceptionDates[key] = stock.getStockPrice(-1, dateToCalculate)
                            if self.cacheExceptionDates[key] == None:
                                if Config.debug():  
                                    print("SignalLineCalculator: Exception check cache")
                                dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                                skipIteration = True
                                break
                        elif self.cacheExceptionDates[key] == None:
                            if Config.debug():  
                                print("SignalLineCalculator: Exception check cache access")
                            dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                            skipIteration = True
                            break
                        
                if skipIteration == True:
                    continue
                
                keyMACDPrice = ticker + "_" + dateToCalculate
                
                if keyMACDPrice not in self.cacheMACD:
                    MACDPrice =self.MACDCalculator.calculateMACD(portfolio, ticker, -1, dateToCalculate)
                    self.cacheMACD[keyMACDPrice] = MACDPrice
                    MACD_prices.append(MACDPrice)
                else:
                    MACD_prices.append(self.cacheMACD[keyMACDPrice])
                                            
                dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                executions += 1

            signalLine = talib.EMA(np.array(MACD_prices), timeperiod=9)
            return MACD_prices[1], round(signalLine[-1], 2)
                
            
