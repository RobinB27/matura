import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.MACDCalculator import MACDCalculator

class SignalLineCalculator:
    
    def __init__(self) -> None:
         self.MACDCalculator = MACDCalculator()
    
    def signalLineCalculation(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateToCalculate: str = "0"):
                #TO DO CHECK IF TICKER VALID AT START
        decision = 0
        #EMA = (todays MACD * K) + (Previous EMA * (1 – K))
        
        signalLine = 0
        weightMultiplier = 2 / (9 + 1)
        MACDPlaceholder = 0
        
        if mode == 0:
            placeHolderDate = date.today()
            if placeHolderDate.isoweekday() > 5:
                print(f"SignalLineCalculator: live calculations not possible on weekend")
                exit()
            
            for stock in portfolio.stocksHeld():
                if stock.name == ticker & stock.getStockPrice() == None:
                    print("SignalLineCalculator: stock market closed (exception date/closing times)")
                    exit()
                    
            MACDPlaceholder = self.MACDCalculator.calculateMACD(portfolio, ticker)
            print(f"MACD: {MACDPlaceholder} on {str(placeHolderDate)}")
            
            MACDAverage = 0
            executions = 0
            
            #subtracting one day from the start for the EMA calculations of the MACD 
            placeHolderDate = placeHolderDate - timedelta(days=1)
            
            while executions < 9:
                if placeHolderDate.isoweekday() > 5:
                    print(f"SignalLineCalculator while loop 0: Weekend: {str(placeHolderDate)}")
                    placeHolderDate = placeHolderDate - timedelta(days=1)
                    continue
                
                placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                getStockPricePlacholderDate = portfolio.addDayToDate(placeHolderDate)
                
                for stock in portfolio.stocksHeld():
                    if stock.name == ticker & stock.getStockPrice(-1, placeHolderDate, getStockPricePlacholderDate) == None:
                        print(f"SignalLineCalculator while loop 0: stock market closed: {str(placeHolderDate)}")
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
                                
            MACDPlaceholder = self.MACDCalculator.calculateMACD(portfolio, ticker, -1, dateToCalculate)
            print(f"SignalLineCalculator: MACD: {MACDPlaceholder} on {dateToCalculate}")
            
            MACDAverage = 0

            #subtracting a day so that 9 MACD average does not include the one already downloaded
            dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
            
            executions = 0
            while executions < 9:
                
                weekendCheck = datetime.strptime(dateToCalculate, "%Y-%m-%d")
                
                if weekendCheck.isoweekday() > 5:
                    print(f"SignalLineCalculator while loop -1: Weekend: {dateToCalculate}")
                    dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                    continue
                
                getStockPricePlacholderDate = portfolio.addDayToDate(dateToCalculate)
                
                for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        if stock.getStockPrice(-1, dateToCalculate, getStockPricePlacholderDate) is None:
                                print(f"SignalLineCalculator while loop -1: exception date: {dateToCalculate}")
                                dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                                continue
                            
                MACDAverage += self.MACDCalculator.calculateMACD(portfolio, ticker, -1, dateToCalculate)
                dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                executions += 1
            
            MACDAverage = MACDAverage / 9

            signalLine = (MACDPlaceholder * weightMultiplier) + (MACDAverage * (1 - weightMultiplier))
            return MACDPlaceholder,signalLine
