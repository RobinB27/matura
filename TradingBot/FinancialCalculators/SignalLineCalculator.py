# This file contains the SignalLineCalculator class. The signal line is part of the so called MACD indicator, a tool to help with trend trading strategies.
# The filee calculates the signal line as well as the MACD itself. To make calculations quicker a chaching system has been used.
# The results of these calculations are the basis with which stock buy/sell decisions are decided (see MACDDecisionmaking.py) according to a MACD indicator trading strategy
import yfinance as fy
import pandas as pd
import numpy as np
import talib
import schedule
import time
    
from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from diskcache import Cache

from Util.Config import Config


class SignalLineCalculator:
    
    def __init__(self) -> None:
        #self.cacheExceptionDates = Cache("./TradingBot/FinancialCalculators/Chaches/cacheExceptionDates")
        #self.cacheStockPrice = Cache("./TradingBot/FinancialCalculators/Caches/StockPriceCache")
        self.stockPrices = []
    
    def signalLineCalculation(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateToCalculate: str = "", intervalTime: int= 0):
                
        if mode == 0:
            self.stockPrices = []
            for i in range(26):
                
                schedule.every(intervalTime).minutes.do(self.job, portfolio, ticker)
            
            schedule.cancel_job(self.job)
            
            macd, signal, hist = talib.MACD(np.array(self.stockPrices), fastperiod=12, slowperiod=26, signalperiod=9)
            return macd[-1], signal[-1]
            
        elif mode == -1:    
            
            for stock in portfolio.stocksHeld:
                    if stock.ticker == ticker:
                        self.stockPrices = stock.getPricesUntilDate(dateToCalculate)

            macd, signal, hist = talib.MACD(np.array(self.stockPrices), fastperiod=12, slowperiod=26, signalperiod=9)
            return macd[-1], signal[-1]

    def job(self, portfolio, ticker ):
        for stock in portfolio.stocksHeld:
                    if stock.ticker == ticker:
                        self.stockPrices.append(stock.getPrice(0))