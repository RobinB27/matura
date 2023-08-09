from TradingBot.Stock import Stock
from datetime import datetime, timedelta, date
import pandas as pd

from Util.Config import Config


class Portfolio:
    """
    defines the portfolio class
    params: fundsAmount
    """
    def __init__(self, fundsAmount):
        
        self.funds = fundsAmount
        self.stocksHeld = [] #could be optimised with a dict
        self.startingFunds = fundsAmount
        
       
    def addStock(self, ticker: str):
        """
        appends the self.stocksHeld list with Stock object using ticker given
        params: ticker
        """
        try:
            
            self.stocksHeld.append(Stock(ticker))
            
        except KeyError:
            raise ValueError("Unrecongnised ticker")
                
    
    #try except clause could be optimised by putting it outside the mode checks
    def buyStock(self, amount: int, nameOfTicker: str, mode: int = 0, date='0'):
        """
        buys the stock if the funds are available, default mode is with live prices,
        past mode buys the stock on one particular day
        params: amount, nameOfTicker, mode (-1 for past mode), dateStart, dateEnd
        """ 
        if mode == 0:
            try:
                for stock in self.stocksHeld:
                #checks if the given stock is a stock held by the portfolio
                    if stock.name == nameOfTicker:
                        currentPrice = stock.getStockPrice()
                        totalCost = currentPrice * amount
                
                    #checks if there are enough funds to buy the stock & buys it
                        if totalCost <= self.funds:
                            self.funds -= totalCost
                            stock.increaseStockAmount(amount)
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
                    if stock.name == nameOfTicker:
                        placeholderEndDate = self.addDayToDate(date)
                        
                        #Returns Open, High, Low, Close, Adj Close, Volume to the
                        historicalStockPrice = stock.getStockPrice(-1, date, placeholderEndDate)
                        totalCost = historicalStockPrice * amount
                        
                        #sells the amount of shares given if enough funds are available
                        if totalCost <= self.funds:
                            self.funds -= totalCost
                            stock.increaseStockAmount(amount)
                            if Config.debug():  
                                print(f"Bought {amount} shares of {nameOfTicker} at ${historicalStockPrice} per share on {date}.")
                        else:
                            if Config.debug():  
                                print("Portfolio: Insufficient funds to buy the stock.")
                
            except KeyError:
                raise ValueError("Unrecongnised ticker")
        
        
    def sellStock(self, amount: int, nameOfTicker: str, mode: int = 0, date='0'):
        """
        sells the stock if the shares are available
        params: amount, nameOfTicker
        """ 
        if mode == 0:
            try:
                for stock in self.stocksHeld:
                    #gets current price of ticker if in portfolio
                    if stock.name == nameOfTicker:
                        currentPrice = stock.getStockPrice()
                        totalPrice = currentPrice * amount
                    
                    #checks if there is enough of a given stock to sell & sells it
                        if stock.amountOfStock >= amount:
                            self.funds += totalPrice
                            stock.decreaseStockAmount(amount)
                            print(f"Sold {amount} shares of {nameOfTicker} at ${currentPrice} per share.")
                        else:
                            print("Insufficient shares to sell the stock.")
            
            except KeyError:
                raise ValueError("Unrecongnised ticker")
        elif mode == -1:
            try:
                #gets historical price of ticker if in portfolio
                for stock in self.stocksHeld:
                    if stock.name == nameOfTicker:
                        
                        placeholderEndDate = self.addDayToDate(date)
                        #Returns historical closing price 
                        historicalStockPrice = stock.getStockPrice(-1, date, placeholderEndDate)
                        totalPrice = historicalStockPrice * amount
                        
                        #sells the amount of shares given
                        if stock.amountOfStock >= amount:
                            self.funds += totalPrice
                            stock.increaseStockAmount(amount)
                            print(f"Sold {amount} shares of {nameOfTicker} at ${historicalStockPrice} per share on {date}.")
                        else:
                            print("Insufficient shares to sell the stock.")
                
            except KeyError:
                raise ValueError("Unrecongnised ticker")
            
    
    def showStocksHeld(self):
        for stock in self.stocksHeld:
            print(stock.name)
            
    def showFundsAvailable(self):
        print(f"Funds inside portfolio: \"{self.name}\" are ${self.funds}")
        
    
    def addDayToDate(self, date: str) -> str:
        """
        adds one day to any given date
        Args: date(str)
        returns: str
        """
        
        date = datetime.strptime(date, "%Y-%m-%d")
        placeholderEndDate = date + timedelta(days=1)
        placeholderEndDate = placeholderEndDate.strftime("%Y-%m-%d")

        return placeholderEndDate
    
    def subtractDayFromDate(self, date: str) -> str:
        """
        subtracts one day to any given date
        Args: date(str)
        returns: str
        """
        
        date = datetime.strptime(date, "%Y-%m-%d")
        placeholderEndDate = date - timedelta(days=1)
        placeholderEndDate = placeholderEndDate.strftime("%Y-%m-%d")

        return placeholderEndDate