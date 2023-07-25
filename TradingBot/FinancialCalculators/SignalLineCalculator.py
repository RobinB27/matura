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
            placeHolderDate = date.today()
            if placeHolderDate.isoweekday() > 5:
                print(f"live calculations not possible on weekend")
                exit()
            
            for stock in portfolio.stocksHeld():
                if stock.name == ticker & stock.getStockPrice() == None:
                    print("stock market closed (exception date/closing times)")
                    exit()
                    
            MACDPlaceholder = self.MACDCalculator.calculateMACD(portfolio, ticker)
            print(f"MACD: {MACDPlaceholder} on {str(placeHolderDate)}")
            
            MACDAverage = 0
            executions = 0
            
            #subtracting one day from the start for the EMA calculations of the MACD 
            placeHolderDate = placeHolderDate - timedelta(days=1)
            
            while executions < 9:
                if placeHolderDate.isoweekday() > 5:
                    print(f"Weekend: {str(placeHolderDate)}")
                    placeHolderDate = placeHolderDate - timedelta(days=1)
                    continue
                
                placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                getStockPricePlacholderDate = portfolio.addDayToDate(placeHolderDate)
                
                for stock in portfolio.stocksHeld():
                    if stock.name == ticker & stock.getStockPrice(-1, placeHolderDate, getStockPricePlacholderDate) == None:
                        print(f"stock market closed (exception date/closing times) on {str(placeHolderDate)}")
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
            FirstCheckPlaceholder1 = datetime.strptime(dateStart, "%Y-%m-%d")
                
            if FirstCheckPlaceholder1.isoweekday() > 5:
                    print(f"Weekend for signal line calculations: {FirstCheckPlaceholder1}")
                    exit()
            
            secondCheckPlaceholder = portfolio.addDayToDate(dateStart)
            
            for stock in portfolio.stocksHeld:
                if stock.name == ticker:
                    if stock.getStockPrice(-1, dateStart, secondCheckPlaceholder) is None:
                                print(f"exception date for signal line calculations: {dateStart} ")
                                exit()
                                
            MACDPlaceholder = self.MACDCalculator.calculateMACD(portfolio, ticker, -1, dateStart)
            print(f"MACD: {MACDPlaceholder} on {dateStart}")
            
            MACDAverage = 0
            placeHolderDate = datetime.strptime(dateStart, "%Y-%m-%d")
            placeHolderDate = placeHolderDate - timedelta(days=1)

            
            executions = 0
            while executions < 9:
                
                if placeHolderDate.isoweekday() > 5:
                    print(f"Weekend for signal line calculations while loop: {placeHolderDate}")
                    placeHolderDate = placeHolderDate - timedelta(days=1)
                    continue
                
                placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                getStockPricePlacholderDate = portfolio.addDayToDate(placeHolderDate)
                
                for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        if stock.getStockPrice(-1, placeHolderDate, getStockPricePlacholderDate) is None:
                                print(f"exception date: {placeHolderDate}")
                                placeHolderDate = portfolio.subtractDayFromDate(placeHolderDate)
                                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                                continue
                                                            
                MACDAverage += self.MACDCalculator.calculateMACD(portfolio, ticker, -1, placeHolderDate)
                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                executions += 1
            
            MACDAverage = MACDAverage / 9

            signalLine = (MACDPlaceholder * weightMultiplier) + (MACDAverage * (1 - weightMultiplier))
            return MACDPlaceholder,signalLine
