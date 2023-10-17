# Copyright (C) 2022 Robin Bacher and Lucien Gees
# This file is part of the "Automated Stock Trading Using News Headlines" matura project.
# Last edited on 17/10/2023

import yfinance as fy
import pandas as pd
from decimal import *

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.Old_Files.LEGACY_SMACalculator import SMACalculator

from diskcache import Cache

from Util.Config import Config


class EMACalculator:
    
    def __init__(self) -> None:
        self.SMACAlculator = SMACalculator()
        self.cache = Cache("./TradingBot/FinancialCalculators/CacheSMA")
        getcontext().prec = 10

    
    def calculateEMA(self, daysToCalculate: int, portfolio: Portfolio, ticker, mode = 0, dateToCalculate:str = ""):
        """Calculates the EMA needed for MACD calculations, 
        EMA(today) = (Close(today) * weightMultiplier) + (EMA(yesterday) * (1 - weightMultiplier))


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
            
            prices = []

            executions = 0
            
            # daysToCalculate - 1 means that the SMA will be used as testing later
            while executions < daysToCalculate - 1:
                
                 #checks if date is a weekend, meaning no price
                placeHolderDate = datetime.strptime(dateToCalculate, "%Y-%m-%d")
                if placeHolderDate.isoweekday() > 5:
                    dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                    continue
                            
                #checks if dateToCalculate is an exception date for stock market closure with cache
                            
                #key for cache
                key = ticker + "_" + dateToCalculate
                
                skipIteration = False
                for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                            
                        if key not in self.cache:
                            self.cache[key] = stock.getStockPrice(-1, dateToCalculate)
                        if self.cache[key] == None:
                            if Config.debug():
                                print("EMACalculator: Exception check cache")
                            dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                            skipIteration = True
                            break
                        elif self.cache[key] == None:
                            if Config.debug():
                                print("EMACalculator: Exception check cache access")
                            dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                            skipIteration = True
                            break  
                if skipIteration == True:
                    continue           
                        
                if Config.debug():  
                    print(f"EMACalculator: Downloading SMA values on: {dateToCalculate}") 
                      
                for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        
                        prices.append(stock.getStockPrice(-1, dateToCalculate))
                
                dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)

                executions += 1
                
            #code for SMA calculation for first EMA value
            
            # checks to ensure SMA is not called on invalid date
            
            SMA_checks_executions = 0
            
            while SMA_checks_executions < 1:
                
                #checks if date is a weekend, meaning no price
                placeHolderDate = datetime.strptime(dateToCalculate, "%Y-%m-%d")
                if placeHolderDate.isoweekday() > 5:
                    dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                    continue
                            
                #checks if dateToCalculate is an exception date for stock market closure with cache
                            
                #key for cache
                key = ticker + "_" + dateToCalculate
                            
                for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                            
                        skipIteration == False
                        if key not in self.cache:
                            self.cache[key] = stock.getStockPrice(-1, dateToCalculate)
                        if self.cache[key] == None:
                            if Config.debug():
                                print("EMACalculator: SMA Calculation Exception check cache")
                            dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                            skipIteration = True
                            break
                        elif self.cache[key] == None:
                            if Config.debug():
                                print("EMACalculator: SMA Calculation Exception check cache access")
                            dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                            skipIteration = True
                            break
                        
                if skipIteration == True:
                    continue
                
                SMA_checks_executions += 1  
            
            #calculation of SMA
            first_EMA = self.SMACAlculator.calculateSMA(daysToCalculate, portfolio, ticker, mode, dateToCalculate)
            
            #insertion of SMA as first EMA value
            prices.insert(0, first_EMA)
            
            
            ema_values = []
            ema_yesterday = prices[0]
       

            #EMA(today) = (Close(today) * α) + (EMA(yesterday) * (1 - α))
                
            for price in prices:
                ema_today = (price * weightMultiplier) + (ema_yesterday * (1 - weightMultiplier))
                ema_values.append(ema_today)
                ema_yesterday = ema_today
                
            ema_value_to_return = round(ema_values[-1], 3)
            return ema_value_to_return