# Copyright (C) 2022 Robin Bacher and Lucien Gees
# This file is part of the "Automated Stock Trading Using News Headlines" matura project.
# Last edited on 17/10/2023

# This file contains the SignalLineCalculator class. The signal line is part of the so called MACD indicator, a tool to help with trend trading strategies.
# The filee calculates the signal line as well as the MACD itself. To make calculations quicker a chaching system has been used.
# The results of these calculations are the basis with which stock buy/sell decisions are decided (see MACDDecisionmaking.py) according to a MACD indicator trading strategy
import yfinance as yf
import numpy as np
import talib 
from datetime import datetime

from TradingBot.Portfolio import Portfolio

from Util.Config import Config


class SignalLineCalculator:
    
    def __init__(self) -> None:
        self.arrayLen = 34 # amount needed determined experimentally for live mode to work
        self.stockPrices = np.zeros(self.arrayLen)
        self.firstRun = True
        
        self.period = "0"

    
    def signalLineCalculation(self, portfolio: Portfolio, ticker: str, mode: int, date: datetime, intervalToTrade: int = None) -> tuple:
        stock = portfolio.getStock(ticker)   
        if mode == 0:
            if self.firstRun:
                
                # determines self.period based on interval given
                
                if 1 <= intervalToTrade < 3600: self.period, intervalToTrade = "5d", f"{intervalToTrade}m"
                else: self.period, intervalToTrade = "3mo", "1d"
                
                # populates self.stockPrices with recent prices
                histData = yf.Ticker(ticker).history(self.period, interval=intervalToTrade)
                selectedPricesForMacd = histData['Close'].tail(self.arrayLen)
                self.stockPrices[:] = selectedPricesForMacd
    
                self.firstRun = False
            else:
                self.stockPrices = self.stockPrices[1:]
                self.stockPrices = np.insert(self.stockPrices, self.arrayLen - 1, stock.getPrice(0))
                        
            macd, signal, hist = talib.MACD(self.stockPrices, fastperiod=12, slowperiod=26, signalperiod=9)
            return macd[-1], signal[-1]
            
        elif mode == -1: 
            self.stockPrices = stock.getPricesUntilDate(date) # more values improve accuracy for talib.MACD
            macd, signal, hist = talib.MACD(np.array(self.stockPrices), fastperiod=12, slowperiod=26, signalperiod=9) #hist needed bc talib.MACD returns 3 values
            return macd[-1], signal[-1]