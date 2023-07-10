import yfinance as fy
import pandas as pd

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.SMACalculator import SMACalculator
from TradingBot.FinancialCalculators.EMACalculator import EMACalculator
from TradingBot.FinancialCalculators.MACDCalculator import MACDCalculator
from TradingBot.FinancialCalculators.SignalLineCalculator import SignalLineCalculator

class MACDDecisionMaking:
    
    
    def __init__(self, mode: int = 0):
        
        self.mode = mode
        self.SMACalculator = SMACalculator()
        self.EmaCalculator = EMACalculator()
        self.MACDCalculator = MACDCalculator()
        self.SignalLineCalculator = SignalLineCalculator()
        
    
    def makeStockDecision(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateStart: str = "0"):
        """makes a decision whether to buy a stock or not on a given date

        Args:
            portfolio (_type_): _description_
            ticker (str): _description_
            mode (int, optional): _description_. Defaults to 0.
            dateStart (str, optional): _description_. Defaults to "0".

        Returns:
            decision in a binary format where 0 is no and 1 is yes
        """
        placeholderResult = self.SignalLineCalculator.signalLineCalculation(portfolio, ticker, mode, dateStart)
        
        MACDPlaceholder = placeholderResult[0]
        signalLine = placeholderResult[1]
        
        if MACDPlaceholder > signalLine:
            decision = 1
        elif MACDPlaceholder < signalLine:
            decision = 0
        
        return decision
           