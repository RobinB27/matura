# This file implements the TemplateDecisionMaking class.
# This class represents a template of a DecisionMaking, which is an implementation of a trading strategy
# in the context of this bot. What is shown in this template is all that is needed for a DecisionMaking class
# to interact seamlessly with the rest of the bot. All other DecisionMaking implementations are based on this template

from datetime import datetime

from TradingBot.Portfolio import Portfolio
from Util.Config import Config


class BuyAndHoldDM:
    """Class that implements a simple Buy and Hold strategy. Sends a buy signal on the first trading step and then ceases operation."""
    
    abbreviation = "B&HDM"
    
    def __init__(self, mode: int = 0):
        
        self.mode = mode
        self.firstRun = True
        
    def makeStockDecision(self, portfolio: Portfolio, ticker: str, mode: int, date: datetime = None, interval: int = 0) -> int:
        """makes a decision whether to buy a stock or not on a given date\n
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
        if self.firstRun:
            if Config.debug(): print(f"DM:\t Stock {ticker} bought")
            self.firstRun = False
            return 1;
        else: return 0