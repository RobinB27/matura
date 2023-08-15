import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.MACDCalculator import MACDCalculator
from diskcache import Cache

from Util.Config import Config


class SignalLineCalculator:
    
    def __init__(self) -> None:
        self.MACDCalculator = MACDCalculator()
        self.cache = Cache("./TradingBot/FinancialCalculators/CacheSMA")

    
    def signalLineCalculation(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateToCalculate: str = ""):
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
            MACD_prices = [MACDPlaceholder]
            
            executions = 0
            dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)

            while executions < 8:
                
                weekendCheck = datetime.strptime(dateToCalculate, "%Y-%m-%d")
                
                if weekendCheck.isoweekday() > 5:
                    if Config.debug():  
                        print(f"SignalLineCalculator while loop -1: Weekend: {dateToCalculate}")
                    dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                    continue
                
                #key for cache
                key = ticker + "_" + dateToCalculate
                skipIteration = False
                for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        if key not in self.cache:
                            self.cache[key] = stock.getStockPrice(-1, dateToCalculate, getStockPricePlacholderDate)
                            if self.cache[key] == None:
                                if Config.debug():  
                                    print("SMACalculator: Exception check cache")
                                dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                                skipIteration = True
                                break
                        elif self.cache[key] == None:
                            if Config.debug():  
                                print("SMACalculator: Exception check cache access")
                            dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                            skipIteration = True
                            break
                        
                if skipIteration == True:
                    continue
                                             
                MACD_prices.append(self.MACDCalculator.calculateMACD(portfolio, ticker, -1, dateToCalculate))
                dateToCalculate = portfolio.subtractDayFromDate(dateToCalculate)
                executions += 1
                
            # Calculate the nine-day EMA of the MACD values
            nine_day_MACD_ema = self.calculateEMA(MACD_prices)
            
            # Replace the MACDAverage calculation with the calculated EMA value
            signalLine = (MACDPlaceholder * weightMultiplier) + (nine_day_MACD_ema * (1 - weightMultiplier))
            return MACDPlaceholder, signalLine

    def calculateEMA(self, MACD_prices):
    
        smoothing_factor = 2 / (9 + 1)
    
        # Initialize the EMA with the first value
        MACD_EMA = []
        MACD_ema_yesterday = MACD_prices[0]
        
        for price in MACD_prices:
            MACD_ema_today = (price * smoothing_factor) + (MACD_ema_yesterday * (1 - smoothing_factor))
            MACD_EMA.append(MACD_ema_today)
            MACD_ema_yesterday = MACD_ema_today
    
        
        return MACD_EMA[-1]