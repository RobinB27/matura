import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.SMACalculator import SMACalculator
from TradingBot.FinancialCalculators.EMACalculator import EMACalculator
from TradingBot.FinancialCalculators.MACDCalculator import MACDCalculator
from TradingBot.FinancialCalculators.SignalLineCalculator import SignalLineCalculator

from consts import debug

class MACDDecisionMaking:
    
    
    def __init__(self, mode: int = 0):
        
        self.mode = mode
        self.SMACalculator = SMACalculator()
        self.EmaCalculator = EMACalculator()
        self.MACDCalculator = MACDCalculator()
        self.SignalLineCalculator = SignalLineCalculator()
        
        self.MACDValuesDict = {}
        self.SingalLineValuesDict = {}
        self.firstRun = True
        self.thirdRunAndBeyond = False
        
        # curveComparison is from perspective of signal line 
        # 1 -> signal line above MACD, 0 -> signal line = MACD, -1 -> signal line below MACD
        self.curveComparison = {}
        
    
    def makeStockDecision(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateToCalculate: str = "0"):
        """makes a decision whether to buy a stock or not on a given date

        Args:
            portfolio (_type_): _description_
            ticker (str): _description_
            mode (int, optional): _description_. Defaults to 0.
            dateStart (str, optional): _description_. Defaults to "0".

        Returns:
            decision in a binary format where 0 is no and 1 is yes
        """
        if self.firstRun == True:
            
            placeholderResult = self.SignalLineCalculator.signalLineCalculation(portfolio, ticker, mode, dateToCalculate)
            
            self.MACDValuesDict[dateToCalculate] = placeholderResult[0]
            self.SingalLineValuesDict[dateToCalculate] = placeholderResult[1]
            
            if self.SingalLineValuesDict[dateToCalculate] > self.MACDValuesDict[dateToCalculate]:
                if debug:
                    print(f"MACDDecisionMaking: MACDPlaceholder: {self.MACDValuesDict[dateToCalculate]} > signalLine: {self.SingalLineValuesDict[dateToCalculate]}")
                self.curveComparison[dateToCalculate] = 1
                
            elif self.SingalLineValuesDict[dateToCalculate] < self.MACDValuesDict[dateToCalculate]:
                if debug:
                    print(f"MACDDecisionMaking: MACDPlaceholder: {self.MACDValuesDict[dateToCalculate]} < signalLine: {self.SingalLineValuesDict[dateToCalculate]}")
                self.curveComparison[dateToCalculate] = -1
                
            else:
                self.curveComparison[dateToCalculate] = 0
            
            self.firstRun = False
            
        elif self.firstRun == False:
    
            placeholderResult = self.SignalLineCalculator.signalLineCalculation(portfolio, ticker, mode, dateToCalculate)
            
            self.MACDValuesDict[dateToCalculate] = placeholderResult[0]
            self.SingalLineValuesDict[dateToCalculate] = placeholderResult[1]

            if self.SingalLineValuesDict[dateToCalculate] > self.MACDValuesDict[dateToCalculate]:
                if debug:
                    print(f"MACDDecisionMaking: MACDPlaceholder: {self.MACDValuesDict[dateToCalculate]} > signalLine: {self.SingalLineValuesDict[dateToCalculate]}")
                self.curveComparison[dateToCalculate] = 1
                
            elif self.SingalLineValuesDict[dateToCalculate] < self.MACDValuesDict[dateToCalculate]:
                if debug:
                    print(f"MACDDecisionMaking: MACDPlaceholder: {self.MACDValuesDict[dateToCalculate]} < signalLine: {self.SingalLineValuesDict[dateToCalculate]}")
                self.curveComparison[dateToCalculate] = -1
                
            else:
                self.curveComparison[dateToCalculate] = 0
                           
            self.thirdRunAndBeyond = True
            
            #to add checks for weekend and exceptions
            previousDate = portfolio.subtractDayFromDate(dateToCalculate)
            
            #checks for crossovers
            while previousDate not in self.curveComparison:
                previousDate = portfolio.subtractDayFromDate(previousDate)
            
            if self.curveComparison[previousDate] == -1 and self.curveComparison[dateToCalculate] == 1:
                if debug:
                    print(f"MACDDecisionMaking: Bullish Crossover on {dateToCalculate}")
                return 1
            elif self.curveComparison[previousDate] == 1 and self.curveComparison[dateToCalculate] == -1:
                if debug:
                    print(f"MACDDecisionMaking: Bearish Crossover on {dateToCalculate}")
                return -1
            else:
                return None
            
        elif self.thirdRunAndBeyond == True:
            pass