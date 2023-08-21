import yfinance as fy

from TradingBot.Portfolio import Portfolio
from Util.Config import Config

class TemplateDecisionMaking:
    
    
    def __init__(self, mode: int = 0):
        
        self.mode = mode
        
    def makeStockDecision(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateToCalculate: str = "0") -> int:
        """makes a decision whether to buy a stock or not on a given date

        Args:
            portfolio (Portfolio): Portfolio to cultivate
            ticker (str): 
            mode (int, optional): Realtime or past mode. Defaults to 0. (past)
            dateStart (str, optional): Starting datestring for past mode. Defaults to "0".

        Returns:
            int: 1 = buy, None = hold, -1 = sell
        """
        
        if Config.debug(): print("Stock Bought")
        return 1;