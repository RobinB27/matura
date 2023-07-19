import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.MACDCalculator import MACDCalculator

class SignalLineCalculator:
    
    def __init__(self) -> None:
         self.MACDCalculator = MACDCalculator()
    
    def signalLineCalculation(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateStart: str = "0"):
                #TO DO CHECK IF TICKER VALID AT START
        decision = 0
        #EMA = (todays MACD * K) + (Previous EMA * (1 – K))
        
        signalLine = 0
        weightMultiplier = 2 / (9 + 1)
        
        MACDPlaceholder = 0
        if mode == 0:
            MACDPlaceholder = self.MACDCalculator.calculateMACD(portfolio, ticker)
            print(f"MACD: {MACDPlaceholder}")
            
            MACDAverage = 0
            placeHolderDate = date.today()
            
            executions = 0
            while executions < 9:
                placeHolderDate = placeHolderDate - timedelta(days=1)
                if placeHolderDate.isoweekday() > 5:
                    continue
                
                placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                MACDAverage += self.MACDCalculator.calculateMACD(portfolio, ticker, -1, placeHolderDate)
                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                executions += 1
            
            MACDAverage = MACDAverage / 9

            signalLine = (MACDPlaceholder * weightMultiplier) + (MACDAverage * (1 - weightMultiplier))
            print(f"SIgnal line: {signalLine}")
            
        elif mode == -1:
            FirstCheckPlaceholder1 = datetime.strptime(dateStart, "%Y-%m-%d")
                
            if FirstCheckPlaceholder1.isoweekday() > 5:
                    print(f"Weekend: {FirstCheckPlaceholder1}")
                    exit()
            
            FirstCheckPlaceholder2 = FirstCheckPlaceholder1
            FirstCheckPlaceholder2 += timedelta(days=1)
            
            FirstCheckPlaceholder1 = FirstCheckPlaceholder1.strftime("%Y-%m-%d")
            FirstCheckPlaceholder2 = FirstCheckPlaceholder2.strftime("%Y-%m-%d")
            
            for stock in portfolio.stocksHeld:
                if stock.name == ticker:
                    if stock.getStockPrice(-1, FirstCheckPlaceholder1, FirstCheckPlaceholder2) is None:
                                print(f"exception date: {FirstCheckPlaceholder1}")
                                exit()
                                
            MACDPlaceholder = self.MACDCalculator.calculateMACD(portfolio, ticker, -1, dateStart)
            print(f"MACD: {MACDPlaceholder}")
            
            MACDAverage = 0
            placeHolderDate = datetime.strptime(dateStart, "%Y-%m-%d")
            
            executions = 0
            while executions < 9:
                
                check = False
                
                placeHolderDate = placeHolderDate - timedelta(days=1)
                
                getStockPricePlacholder = placeHolderDate
                getStockPricePlacholder += timedelta(days=1)
                getStockPricePlacholder = getStockPricePlacholder.strftime("%Y-%m-%d")
                
                if placeHolderDate.isoweekday() > 5:
                    print(f"Weekend: {placeHolderDate}")
                    continue
                placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        if stock.getStockPrice(-1, placeHolderDate, getStockPricePlacholder) is None:
                                print(f"exception date: {placeHolderDate}")
                                check = True
                                continue
                            
                if check == True:
                    placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                    continue
                                
                MACDAverage += self.MACDCalculator.calculateMACD(portfolio, ticker, -1, placeHolderDate)
                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                executions += 1
            
            MACDAverage = MACDAverage / 9

            signalLine = (MACDPlaceholder * weightMultiplier) + (MACDAverage * (1 - weightMultiplier))
            return MACDPlaceholder,signalLine
