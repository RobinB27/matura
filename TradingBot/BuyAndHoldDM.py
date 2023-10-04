# This file implements the TemplateDecisionMaking class.
# This class represents a template of a DecisionMaking, which is an implementation of a trading strategy
# in the context of this bot. What is shown in this template is all that is needed for a DecisionMaking class
# to interact seamlessly with the rest of the bot. All other DecisionMaking implementations are based on this template

import yfinance as fy
from datetime import datetime

from TradingBot.Portfolio import Portfolio
from Util.Config import Config

class BuyAndHoldDM:
    
    
    def __init__(self, mode: int = 0):
        
        self.mode = mode
        self.run = 1
        
    def makeStockDecision(self, portfolio: Portfolio, ticker: str, mode: int, date: datetime = None, interval: int = 0) -> int:
        """makes a decision whether to buy a stock or not on a given date,
        in this strategy only one of each stock is bought and nothing else

        Args:
            portfolio (Portfolio): Portfolio to cultivate
            ticker (str): stock ticker name
            mode (int, optional): Realtime or historical data mode.
            date (datetime, optional): date required for historical data mode. Defaults to None.
            interval (int, optional): interval required for realtime mode. Defaults to 0

        Returns:
            int: 1 = buy, -1 = sell, any other value = ignore stock 
        """
        if self.run == 1:
            if Config.debug(): print("Stock Bought")
            self.run += 1
            return 1;
        else:
            return 0