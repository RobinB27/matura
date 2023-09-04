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
        self.arrayLen = 34 # amount determined experimentally
        self.stockPrices = np.zeros(self.arrayLen)
        self.firstRun = True
    
    def signalLineCalculation(self, portfolio: Portfolio, ticker: str, mode: int, date: datetime, intervalToTrade: int= 0) -> tuple:
        stock = portfolio.getStock(ticker)   
        if mode == 0:
            if self.firstRun:
                histData = yf.Ticker(ticker).history(period= "7d", interval=f"{intervalToTrade}m")
                selectedPricesForMacd = histData['Close'].tail(self.arrayLen)
                self.stockPrices[:] = selectedPricesForMacd
    
                self.firstRun = False
            else:
                self.stockPrices = self.stockPrices[1:]
                self.stockPrices = np.insert(self.stockPrices, self.arrayLen - 1, stock.getPrice(0))
                        
            macd, signal, hist = talib.MACD(self.stockPrices, fastperiod=12, slowperiod=26, signalperiod=9)
            return macd[-1], signal[-1]
            
        elif mode == -1: 
            self.stockPrices = stock.getPricesUntilDate(date)
            macd, signal, hist = talib.MACD(np.array(self.stockPrices), fastperiod=12, slowperiod=26, signalperiod=9) #hist needed bc talib.MACD returns 3 values
            return macd[-1], signal[-1]