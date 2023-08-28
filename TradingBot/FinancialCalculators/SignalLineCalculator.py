# This file contains the SignalLineCalculator class. The signal line is part of the so called MACD indicator, a tool to help with trend trading strategies.
# The filee calculates the signal line as well as the MACD itself. To make calculations quicker a chaching system has been used.
# The results of these calculations are the basis with which stock buy/sell decisions are decided (see MACDDecisionmaking.py) according to a MACD indicator trading strategy
import yfinance as fy
import pandas as pd
import numpy as np
import talib

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from diskcache import Cache

from Util.Config import Config


class SignalLineCalculator:
    
    def __init__(self) -> None:
        self.cacheExceptionDates = Cache("./TradingBot/FinancialCalculators/Chaches/cacheExceptionDates")
        self.cacheStockPrice = Cache("./TradingBot/FinancialCalculators/Caches/StockPriceCache")
    
    def signalLineCalculation(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateToCalculate: str = ""):
                
        if mode == 0:
            pass
            
        elif mode == -1:    
                        
            stockPrices = []
            
            for stock in portfolio.stocksHeld:
                    if stock.ticker == ticker:
                        stockPrices = stock.getPricesUntilDate(dateToCalculate)

            macd, signal, hist = talib.MACD(np.array(stockPrices), fastperiod=12, slowperiod=26, signalperiod=9)
            return macd[-1], signal[-1]
