# Copyright (C) 2022 Robin Bacher and Lucien Gees
# This file is part of the "Automated Stock Trading Using News Headlines" matura project.
# Last edited on 17/10/2023

# This File contains the Stock class. It is a virtual representation of any given Stock (Aktie) that is listed on the NYSE or NASDAQ stock exchange.
# This means that it keeps track of the amount of stock owned, it can fetch the stock's price on any given date (or real time), and you can buy/sell a stock
# The stock objects created by this function are held in another type of class called Portfolio (see Portfolio.py) inside a list of other stocks.
# This file is important for the overarching project because it is the fundamental building block for all trading activities and since it gets all stock prices

from datetime import datetime
from diskcache import Cache
import yfinance as yf


from Util.Config import Config
from Util.DateHelper import DateHelper

class Stock:
    """ 
    Class representing an amount of a specific stock.\n 
    This type is used by the Portfolio class.
    """

    def __init__(self, ticker: str):
        """Creates a new instance of the Stock class.\n 
        checks Ticker validity.

        Args:
            ticker (str): Stock Ticker, e.g. "TSLA"

        Raises:
            ValueError: Raised if ticker input is invalid
        """
        
        self.ticker = ticker
        self.amount = 0
        self.cache = Cache(f"./TradingBot/Stock_Caches/Cache{ticker.capitalize()}")
        self.stockHistCache = Cache(f"./TradingBot/Stock_Hist_Caches/CacheStockHist{ticker.capitalize()}")
        
        try:
            if len(self.stockHistCache) == 0:
                
                # Check ticker validity           
                try:self.tickerInfo = yf.Ticker(ticker).info
                except KeyError: raise ValueError("Stock:\t Error: Unrecongnised ticker")
                except ConnectionError: raise ConnectionError("No wifi connection")
                
                self.stockHistCache["stockHist"] = yf.Ticker(ticker).history(period="max")
        except ConnectionError: raise ConnectionError("No wifi connection")
            
        
        # Cache persist over sessions. If a cache is generated in, say, October 2023, the cache will be limited to the prices generated until October 2023.
        if len(self.cache) == 0:
            # uses self.stockHistCache to not need wifi for self.cache population
            for index in self.stockHistCache["stockHist"].index:
                key = index.strftime("%Y-%m-%d") # NOTE key is the same format as date
                self.cache[key] = self.stockHistCache["stockHist"].loc[index, "Close"]



    def getPrice(self, mode: int, date: datetime = None) -> int:
        """Fetches stock prices for a specific date.

        Args:
            mode (int, optional): real time (0) or historical data (-1).
            date (str, optional): date, required for historical data.

        Returns:
            int: stock price, or None if no price could be fetched.
        """
        if mode == 0:
            # Ticker info must be fetched anew on each function call to ensure the data is current
            currentInfo = yf.Ticker(self.ticker).info
            try:
                stockPrice = currentInfo.get("currentPrice") # NOTE might cause a mystery issue -> should be fixed Mon 9th Oct 2023
                if Config.debug():
                    print(f"Stock:\t Current stock price of {self.ticker} is {stockPrice}")
                return stockPrice
            except KeyError:
                if Config.debug():
                    print(f"Stock:\t Error: Market currently not open")
                return None

        elif mode == -1 and date is not None:
            date = DateHelper.format(date)
             
            try:
                closing_price = self.cache[date] # NOTE date is equivalent to key above
                return closing_price
            except KeyError:
                if Config.debug():
                    print(f"Stock:\t Exception date caught: {date}")
                return None
        elif date is None:
            raise KeyError("Stock:\t Error: fetching stock prices in past mode requires a date to be specified.")

    def getPricesUntilDate(self, date: datetime):
        """fetches past stock prices for a period of time
        (Ending date inclusive)
        Args: start date ('year-month-day')

        Args:
            dateToCalculate (str): the last date of prices

        Returns:
            _type_: list -> int
        """
        date = DateHelper.format(date)
        historical_data = self.stockHistCache["stockHist"]
        # Removes NaN rows
        historical_data = historical_data.dropna()
        historical_data = historical_data[historical_data.index <= date]
        prices = historical_data['Close'].to_list()
        return prices

    def increase(self, amount: int) -> None:
        """Increase the amount of this stock.

        Args:
            amount (int): amount to increase
        """
        self.amount += amount

    def decrease(self, amount: int) -> None:
        """Decrease the amount of this stock.

        Args:
            amount (int): amount to decrease
        """
        if self.amount - amount >= 0: self.amount -= amount
        else: 
            if Config.debug():
                print("Stock:\t Insufficient amount of stock to sell.")
                
    def clearCaches(self) -> None:
        """utility method that clears all the stocks caches
        """
        self.cache.clear()
        self.stockHistCache.clear()
