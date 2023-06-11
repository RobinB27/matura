import yfinance as fy
from datetime import datetime, timedelta, date
import pandas as pd
from TradingBot.Portfolio import Portfolio

class MACDDecisionMaking:
    
    def __init__(self, mode: int = 0, startDate: str = "0"):
        
        self.date = startDate
        
    
    def makeStockDecision(self):
        
        decision = 0
        
        
        return decision
    
    def calculateMACD(self, mode: int = 0, date: str = "0"):
        pass