# Copyright (C) 2022 Robin Bacher and Lucien Gees
# This file is part of the "Automated Stock Trading Using News Headlines" matura project.
# Last edited on 17/10/2023

# This file implements the TemplateDecisionMaking class.
# This class represents a template of a DecisionMaking, which is an implementation of a trading strategy
# in the context of this bot. What is shown in this template is all that is needed for a DecisionMaking class
# to interact seamlessly with the rest of the bot. All other DecisionMaking implementations are based on this template

from datetime import datetime

from TradingBot.Portfolio import Portfolio
from Util.Config import Config


class TemplateDM:
    """
    Replace this docstring with a description of the implemented strategy
    """

    def __init__(self, mode: int = 0):
        self.mode = mode

    def makeStockDecision(self, portfolio: Portfolio, ticker: str, mode: int, date: datetime = None, interval: int = 0) -> int:
        """makes a decision whether to buy a stock or not on a given date, must be implemented for a strategy to work.

        Args:
            portfolio (Portfolio): Associated portfolio class
            ticker (str): stock ticker name
            mode (int): Realtime or historical data mode. (0, -1)
            date (datetime, optional): date required for historical data mode. Defaults to None.
            interval (int, optional): interval required for realtime mode. Defaults to 0

        Returns:
            int: The signal produced by the trading strategy. Format: 1 = buy, -1 = sell, None or any other value = ignore stock 
        """

        # sample code
        # Please follow this console format and the return types states in the docstring.
        if Config.debug():
            print(f"DM:\t Stock {ticker} Bought")
        return 1
