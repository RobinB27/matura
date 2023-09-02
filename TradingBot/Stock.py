# This File contains the Stock class. It is a virtual representation of any given Stock (Aktie) that is listed on the NYSE or NASDAQ stock exchange.
# This means that it keeps track of the amount of stock owned, it can fetch the stock's price on any given date (or real time), and you can buy/sell a stock
# The stock objects created by this function are held in another type of class called Portfolio (see Portfolio.py) inside a list of other stocks.
# This file is important for the overarching project because it is the fundamental building block for all trading activities and since it gets all stock prices

from datetime import datetime
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
        self.tickerObject = yf.Ticker(ticker)
        self.stockHist = self.tickerObject.history(period="max")

        # Check ticker validity
        try:self.tickerInfo = self.tickerObject.info
        except KeyError: raise ValueError("Stock:\t Error: Unrecongnised ticker")

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
                stockPrice = currentInfo.get("currentPrice")
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
                closing_price = self.stockHist.loc[date, "Close"]
                if Config.debug():
                    print(f"Stock:\t Stock price of {self.ticker} is {closing_price} on {date}")
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
        try:
            historical_data = self.tickerObject.history(period="max")
            # Removes NaN rows
            historical_data = historical_data.dropna()
            historical_data = historical_data[historical_data.index <= date]
            prices = historical_data['Close'].to_list()
            return prices

        except KeyError:
            if Config.debug():
                print(f"Stock:\t exception date: {date}")
            return {}  # NOTE: does returning this on an error make sense? Shouldn't the programme cancel?

    # NOTE: Is this used / needed? Would like to remove
    def displayAmount(self) -> None:
        """displays the stock class attribute amountOfStock for debugging purposes"""
        print(f"Stock:\t Number of {self.ticker} owned: {self.amount}")

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
