# Copyright (C) 2022 Robin Bacher and Lucien Gees
# This file is part of the "Automated Stock Trading Using News Headlines" matura project.
# Last edited on 17/10/2023

import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio
from diskcache import Cache

from TradingBot.FinancialCalculators.Old_Files.LEGACY_EMACalculator import EMACalculator

from Util.Config import Config


class MACDCalculator:
    
    def __init__(self):
        self.EMACalculator = EMACalculator()
        self.cache = Cache("./TradingBot/FinancialCalculators/Caches/CacheEMA12")
        self.cache = Cache("./TradingBot/FinancialCalculators/Caches/CacheEMA26")

    
    def calculateMACD(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateToCalculate: str = "0"):
        
        # MACD = 12 day EMA - 26 day EMA
        # EMA = exponential moving average
        
        # thought that maybe two modes arent needed because the code in mode = 0 should work for every date given (needs testing)
        # the above thought isnt possible due to the way the getStockPrice() function is implemented
        
        # mode is currently using the function param mode, couldn't this be the class variable?
        
        if mode == 0:
            
            if Config.debug():  
                print(f"MACDCalculator: Downloading EMA 12")
            EMA_Placeholder12days = self.EMACalculator.calculateEMA(12, portfolio, ticker)
            if Config.debug():  
                print(f"MACDCalculator: Downloading EMA 26")
            EMA_Placeholder26days = self.EMACalculator.calculateEMA(26, portfolio, ticker)

            MACDline = EMA_Placeholder12days - EMA_Placeholder26days
            return MACDline
            
            
            
        elif mode == -1:
            
            key12 = ticker + "_" + dateToCalculate + "_12"
            key26 = ticker + "_" + dateToCalculate + "_26"
            
            if key12 not in self.cache:
                if Config.debug():  
                    print(f"MACDCalculator: Downloading EMA 12: {dateToCalculate}")
                EMA12OnDate = self.EMACalculator.calculateEMA(12, portfolio, ticker, -1, dateToCalculate)
                self.cache[key12] = EMA12OnDate  
            else:
                if Config.debug():  
                    print(f"MACDCalculator: Accessing Cache for EMA 12: {dateToCalculate}")
                EMA12OnDate = self.cache[key12]
            
            if key26 not in self.cache:
                if Config.debug():  
                    print(f"MACDCalculator: Downloading EMA 26: {dateToCalculate}")
                EMA26OnDate = self.EMACalculator.calculateEMA(26, portfolio, ticker, -1, dateToCalculate)
                self.cache[key26] = EMA26OnDate  
            else:
                if Config.debug():  
                    print(f"MACDCalculator: Accessing Cache for EMA 26: {dateToCalculate}")
                EMA26OnDate = self.cache[key26]
                
            MACDline = EMA12OnDate - EMA26OnDate 
            return round(MACDline, 2)                        