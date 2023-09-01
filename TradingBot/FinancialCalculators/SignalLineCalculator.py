# This file contains the SignalLineCalculator class. The signal line is part of the so called MACD indicator, a tool to help with trend trading strategies.
# The filee calculates the signal line as well as the MACD itself. To make calculations quicker a chaching system has been used.
# The results of these calculations are the basis with which stock buy/sell decisions are decided (see MACDDecisionmaking.py) according to a MACD indicator trading strategy
import yfinance as yf
import pandas as pd
import numpy as np
import talib

    
from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from diskcache import Cache

from Util.Config import Config


class SignalLineCalculator:
    
    def __init__(self) -> None:
        self.amountOfDataNeededForMACDCalculations = 34 #amount determined experimentally
        self.stockPrices = np.zeros(self.amountOfDataNeededForMACDCalculations)
        self.run = 0
    
    def signalLineCalculation(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateToCalculate: str = "", intervalToTrade: int= 0):
                
        if mode == 0:
            if self.run == 0:
                for stock in portfolio.stocksHeld:
                    if stock.ticker == ticker:
                        histData = yf.Ticker(ticker).history(period= "7d", interval=f"{intervalToTrade}m")
                        selectedPricesForMacd = histData['Close'].tail(self.amountOfDataNeededForMACDCalculations)
                        self.stockPrices[:] = selectedPricesForMacd
    
                self.run += 1
            elif self.run >= 1:
                for stock in portfolio.stocksHeld:
                    if stock.ticker == ticker:
                        self.stockPrices = self.stockPrices[1:]
                        self.stockPrices = np.insert(self.stockPrices, self.amountOfDataNeededForMACDCalculations - 1, stock.getPrice(0))
                        
            macd, signal, hist = talib.MACD(self.stockPrices, fastperiod=12, slowperiod=26, signalperiod=9)
            return macd[-1], signal[-1]
            
        elif mode == -1:    
            
            for stock in portfolio.stocksHeld:
                    if stock.ticker == ticker:
                        self.stockPrices = stock.getPricesUntilDate(dateToCalculate)

            macd, signal, hist = talib.MACD(np.array(self.stockPrices), fastperiod=12, slowperiod=26, signalperiod=9)
            return macd[-1], signal[-1]