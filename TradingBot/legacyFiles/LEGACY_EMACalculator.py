# Copyright (C) 2022 Robin Bacher and Lucien Gees
# This file is part of the "Automated Stock Trading Using News Headlines" matura project.
# Last edited on 17/10/2023

import yfinance as fy
import pandas as pd
import numpy as np
import talib

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from diskcache import Cache

from Util.Config import Config


class EMACalculator:
    
    def __init__(self) -> None:
        self.cacheExceptionDates = Cache("./TradingBot/FinancialCalculators/Chaches/cacheExceptionDates")

    
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
            pass
            
        elif mode == -1:
            
            executions = 0 
            # daysToCalculate - 1 means that the SMA will be used as testing later
            while executions < 1:
                
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
                        if key not in self.cacheExceptionDates:
                            self.cacheExceptionDates[key] = stock.getStockPrice(-1, dateToCalculate)
                        if self.cacheExceptionDates[key] == None:
                            if Config.debug():
                                print("EMACalculator: Exception check cache")
                            dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                            skipIteration = True
                            break
                        elif self.cacheExceptionDates[key] == None:
                            if Config.debug():
                                print("EMACalculator: Exception check cache access")
                            dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                            skipIteration = True
                            break  
                        
                if skipIteration == True:
                    continue                  

                executions += 1
                
            for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        historical_data = stock.getStockPricesUntilDate(dateToCalculate)
                            
            closing_prices = list(historical_data.values())
            
            #EMA = (todays MACD * K) + (Previous EMA * (1 – K))
            ema_values = talib.EMA(np.array(closing_prices), timeperiod=daysToCalculate)

            return round(ema_values[-1], 2)