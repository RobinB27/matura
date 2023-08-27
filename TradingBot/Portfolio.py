from TradingBot.Stock import Stock
from datetime import datetime, timedelta, date
import pandas as pd

from Util.Config import Config


class Portfolio:
    """
    defines  portfolio class, holds stocks, buy/sell stocks, keeps track of funds
    params: fundsAmount
    """
    def __init__(self, fundsAmount):
        """constructor of portfolio class
        Args:
            fundsAmount (int): starting funds of portfolio
        """
        
        self.funds = fundsAmount
        self.stocksHeld = [] #could be optimised with a dict
        self.startingFunds = fundsAmount
        
       
    def addStock(self, ticker: str):
        """
        appends the self.stocksHeld list with Stock object using ticker given
        args:
            params (str): name of stockticker
        """
        try:
            self.stocksHeld.append(Stock(ticker))           
        except KeyError:
            raise ValueError("Unrecongnised ticker")
                
    
    #try except clause could be optimised by putting it outside the mode checks
    def buyStock(self, amount: int, nameOfTicker: str, mode: int = 0, date='0'):
        """buys the stock if funds available, default mode live prices,
        past mode buys stock with historical price data on date given
        Args:
            amount (int): amount of stock to buy
            nameOfTicker (str): name of stock ticker
            mode (int, optional): live(0) or past mode (-1). Defaults to 0.
            date (str, optional): date for past mode. Defaults to '0'.

        Raises:
            ValueError: invalid ticker name
            ValueError: invalid ticker name
        """
        if mode == 0:
            try:
                for stock in self.stocksHeld:
                #checks if the given stock is a stock held by the portfolio
                    if stock.ticker == nameOfTicker:
                        currentPrice = stock.getPrice()
                        totalCost = currentPrice * amount
                
                    #checks if there are enough funds to buy the stock & buys it
                        if totalCost <= self.funds:
                            self.funds -= totalCost
                            stock.increase(amount)
                            if Config.debug():  
                                print(f"Bought {amount} shares of {nameOfTicker} at ${currentPrice} per share.")
                        else:
                            if Config.debug():  
                                print("Portfolio: Insufficient funds to buy the stock.")
            
            except KeyError:
                raise ValueError("Unrecongnised ticker")
        
        elif mode == -1:
            try:
                #gets historical price if ticker in portfolio
                for stock in self.stocksHeld:
                    if stock.ticker == nameOfTicker:
                        
                        #Returns Open, High, Low, Close, Adj Close, Volume to the
                        historicalStockPrice = stock.getPrice(-1, date)
                        totalCost = historicalStockPrice * amount
                        
                        #sells the amount of shares given if enough funds are available
                        if totalCost <= self.funds:
                            self.funds -= totalCost
                            stock.increase(amount)
                            if Config.debug():  
                                print(f"Bought {amount} shares of {nameOfTicker} at ${historicalStockPrice} per share on {date}.")
                        else:
                            if Config.debug():  
                                print("Portfolio: Insufficient funds to buy the stock.")
                
            except KeyError:
                raise ValueError("Unrecongnised ticker")
        
        
    def sellStock(self, amount: int, nameOfTicker: str, mode: int = 0, date='0'):
        """sells the stock if stock class attribute amountOfStock sufficent, default mode live prices,
        past mode sells stock with historical price data on date given

        Args:
            amount (int): amount to sell
            nameOfTicker (str): name of ticker to sell
            mode (int, optional): live(0) or past (-1) mode. Defaults to 0.
            date (str, optional): date for past mode. Defaults to '0'.

        Raises:
            ValueError: invalid ticker name
            ValueError: invalid ticker name
        """
        if mode == 0:
            try:
                for stock in self.stocksHeld:
                    #gets current price of ticker if in portfolio
                    if stock.ticker == nameOfTicker:
                        currentPrice = stock.getPrice()
                        totalPrice = currentPrice * amount
                    
                    #checks if there is enough of a given stock to sell & sells it
                        if stock.amount >= amount:
                            self.funds += totalPrice
                            stock.decrease(amount)
                            print(f"Sold {amount} shares of {nameOfTicker} at ${currentPrice} per share.")
                        else:
                            print("Insufficient shares to sell the stock.")
            
            except KeyError:
                raise ValueError("Unrecongnised ticker")
        elif mode == -1:
            try:
                #gets historical price of ticker if in portfolio
                for stock in self.stocksHeld:
                    if stock.ticker == nameOfTicker:
                        
                        #Returns historical closing price 
                        historicalStockPrice = stock.getPrice(-1, date)
                        totalPrice = historicalStockPrice * amount
                        
                        #sells the amount of shares given
                        if stock.amount >= amount:
                            self.funds += totalPrice
                            stock.decrease(amount)
                            print(f"Sold {amount} shares of {nameOfTicker} at ${historicalStockPrice} per share on {date}.")
                        else:
                            print("Insufficient shares to sell the stock.")
                
            except KeyError:
                raise ValueError("Unrecongnised ticker")
            
    
    def showStocksHeld(self):
        """until method to display all stocks held in portfolio
        """
        for stock in self.stocksHeld:
            print(stock.ticker)
            
    def showFundsAvailable(self):
        print(f"Funds inside portfolio: \"{self.name}\" are ${self.funds}")
        
    
    def addDayToDate(self, date: str) -> str:
        """
        adds one day to any given date
        Args: date(str)
        returns: date(str)
        """
        
        date = datetime.strptime(date, "%Y-%m-%d")
        placeholderEndDate = date + timedelta(days=1)
        placeholderEndDate = placeholderEndDate.strftime("%Y-%m-%d")

        return placeholderEndDate
    
    def subtractDayFromDate(self, date: str) -> str:
        """
        subtracts one day from any given date
        Args: date(str)
        returns: date(str)
        """
        
        date = datetime.strptime(date, "%Y-%m-%d")
        placeholderEndDate = date - timedelta(days=1)
        placeholderEndDate = placeholderEndDate.strftime("%Y-%m-%d")

        return placeholderEndDate
    
    def subtractMultipleDaysFromDate(self, date: str, daysToSubtract) -> str:
        """
        subtracts multiple days from any given date
        Args: date(str)
        returns: str
        """
        #double weekendcheck to ensure that it's not a weekend after an exception date
        for i in range(daysToSubtract):
            date = datetime.strptime(date, "%Y-%m-%d")
            date = date - timedelta(days=1)
            date = date.strftime("%Y-%m-%d")
        
        date = datetime.strptime(date, "%Y-%m-%d")
        
        while date.isoweekday() > 5:
            date = date - timedelta(days=1)
            
        exceptionCheck = date.strftime("%Y-%m-%d")
        
        TSLA = Stock("TSLA")    
        if TSLA.getPrice(-1, exceptionCheck) is None:
            date = date - timedelta(days=1)
                    
        while date.isoweekday() > 5:
            date = date - timedelta(days=1)
            
        date = date.strftime("%Y-%m-%d")  
        return date