# Copyright (C) 2022 Robin Bacher and Lucien Gees
# This file is part of the "Automated Stock Trading Using News Headlines" matura project.
# Last edited on 17/10/2023

# This file contains the Portfolio class. It is a virtual representation of a stock portfolio that holds a number of user given stocks (see Stock.py file).
# The portfolio class keeps track of all stocks owned and the amount of funds inside of it for later reference.
# Furthermore, the class has the ability to buy/sell stocks. This decreases/increases the funds inside the portfolio and decreases the amount of stock owned (Stock class attribute)
# It ties into the bot as the medium through which stock decisions are implemented

from datetime import datetime, timedelta

from TradingBot.Stock import Stock

from Util.DateHelper import DateHelper
from Util.Config import Config


class Portfolio:
    """
    Class representing a Portfolio of stocks.\n
    Keeps track of all stocks held and provides methods for buying and selling.
    """
    
    def __init__(self, funds):
        """Creates a new instance of the Portfolio class.
        
        Args:
            funds (int): starting funds of portfolio
        """
        
        self.funds = funds
        self.stocksHeld = {}
        self.startingFunds = funds
    
    def getStocks(self) -> list:
        """Shorthand to get stocksHeld in list form

        Returns:
            list[Stock]: Contains all stocks held.
        """
        return list(self.stocksHeld.values())
        
    def getStock(self, ticker:str) -> Stock:
        """Utility function to retrieve Stock class from Portfolio.

        Args:
            ticker (str): Stock ticker
            
        Returns:
            Stock: searched Stock instance

        Raises:
            KeyError: Stock is not included in the Portfolio.
        """
        if ticker in self.stocksHeld: return self.stocksHeld[ticker]
        else: raise KeyError("Portf\t Error: Tried to buy Stock not included in the Portfolio.")
       
    def addStock(self, ticker: str):
        """Adds a stock to the porfolio
        args:
            params (str): name of stockticker
        """
        if ticker not in self.stocksHeld:
            self.stocksHeld[ticker] = Stock(ticker)
        else: raise KeyError("Portf\t Error: Tried to add Stock to portfolio that is already included")
    
    def buyStock(self, amount: int, ticker: str, mode: int, date: datetime = None):
        """Buys a stock and adds it to the Portfolio.\n
        either at historical or current price depending on mode.\n
        Args:
            amount (int): amount of stock to buy
            ticker (str): name of stock ticker
            mode (int): realtime (0) or historical data (-1).
            date (str, optional): date, required for historical data mode (-1). Defaults to None.

        Raises:
            KeyError: Raised when trying to buy a stock not in the portfolio
        """
            
        # selects either current or historical price depending on mode
        stock: Stock = self.getStock(ticker)
        currentPrice = stock.getPrice(mode, date)
                
        #checks if there are enough funds to buy the stock & buys it
        cost = currentPrice * amount
        if cost <= self.funds:
            self.funds -= cost
            stock.increase(amount)
            if Config.debug() and mode == 0:
                print(f"Portf:\t Bought {amount} shares of {ticker} at ${currentPrice} per share.")
            elif Config.debug() and mode == -1:
                print(f"Portf:\t Bought {amount} shares of {ticker} at ${currentPrice} per share on {DateHelper.format(date)}.")
        else:
            if Config.debug():  
                print("Portf:\t Error: Insufficient funds to buy the stock.")
        
        
    def sellStock(self, amount: int, ticker: str, mode: int,  date: datetime = None):
        """Sells a stock in the Portfolio.\n
        either at historical or at current price depending on mode.\n

        Args:
            amount (int): amount to sell
            ticker (str): name of ticker to sell
            mode (int): realtime (0) or historical data (-1).
            date (str, optional): date, required for historical data mode. Defaults to None.

        Raises:
            KeyError: Raised when trying to sell a stock not in the portfolio
        """

        #gets current price of ticker if in portfolio
        stock: Stock = self.getStock(ticker)
        currentPrice = stock.getPrice(mode, date)
                    
        #checks if there is enough of a given stock to sell & sells it
        price = currentPrice * amount
        if stock.amount >= amount:
            self.funds += price
            stock.decrease(amount)
            if Config.debug() and mode == 0:
                print(f"Portf:\t Sold {amount} shares of {ticker} at ${currentPrice} per share.")
            elif Config.debug() and mode == -1:
                print(f"Portf:\t Sold {amount} shares of {ticker} at ${currentPrice} per share on {DateHelper.format(date)}.")
        else:
            if Config.debug():
                print("Portf\t Error: Insufficient shares to sell the stock.")

