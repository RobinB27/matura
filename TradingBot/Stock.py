# This File contains the Stock class. It is a virtual representation of any given Stock (Aktie) that is listed on the NYSE or NASDAQ stock exchange.
# This means that it keeps track of the amount of stock owned, it can fetch the stock's price on any given date (or real time), and you can buy/sell a stock
# The stock objects created by this function are held in another type of class called Portfolio (see Portfolio.py) inside a list of other stocks.
# This file is important for the overarching project because it is the fundamental building block for all trading activities and since it gets all stock prices

import yfinance as yf

from Util.Config import Config


class Stock:
    """
    Class representing an amount of a specific stock. This type is used by the Portfolio class.
    """

    def __init__(self, ticker: str):
        """Creates a new instance of the Stock class, checks Ticker validity.

        Args:
            ticker (str): Stock Ticker, e.g. "TSLA"

        Raises:
            ValueError: Raised if ticker input is invalid
        """
        self.ticker = ticker
        self.amount = 0
        self.tickerObject = yf.Ticker(ticker)
        self.stockInfo = self.tickerObject.history(period="max")

        # Check ticker validity
        try:
            self.tickerInfo = self.tickerObject.info
        except KeyError:
            raise ValueError("Unrecongnised ticker")

    def getPrice(self, mode: int = 0, date: str = '0') -> int:
        """Fetches stock prices for a specific date.

        Args:
            mode (int, optional): live (0) or past mode (-1). Defaults to 0.
            dateStart (str, optional): date to fetch prices.

        Returns:
            int: stock price
        """
        if mode == 0:
            #always ensured that not used when market closed
            placeholder = yf.Ticker(self.ticker).info
            try:
                stockPrice = placeholder.get("currentPrice")
                if Config.debug():
                    print(f"Stock:\t Current stock price of {self.ticker} is {stockPrice}")
            except KeyError:
                if Config.debug():
                    print(f"Stock:\t Error: Market not open/Exception date")

            return stockPrice

        elif mode == -1:
            try:
                closing_price = self.stockInfo.loc[date, "Close"]

                if Config.debug():
                    print(f"Stock:\t Stock price of {self.ticker} is {closing_price} on {date}")

                return closing_price

            except KeyError:
                if Config.debug():
                    print(f"Stock: exception date: {date}")
                return None

    def getPricesUntilDate(self, dateToCalculate: str):
        """fetches past stock prices for a period of time
        (Ending date inclusive)
        Args: start date ('year-month-day') #NOTE: datetimes

        Args:
            dateToCalculate (str): the last date of prices

        Returns:
            _type_: list -> int
        """
        try:
            historical_data = self.tickerObject.history(period="max")
            # Removes NaN rows
            historical_data = historical_data.dropna()
            historical_data = historical_data[historical_data.index <= dateToCalculate]
            prices = historical_data['Close'].to_list()
            return prices

        except KeyError:
            if Config.debug():
                print(f"Stock:\t exception date: {dateToCalculate}")
            return {}  # NOTE: does returning this on an error make sense? Shouldn't the programme cancel?

    def displayAmount(self) -> None:
        """displays the stock class attribute amountOfStock for debugging purposes"""
        print(f"Number of {self.ticker} owned: {self.amount}")

    def increase(self, amount: int) -> None:
        """increases stock class attribute amountOfStock 

        Args:
            amount (int): amount to increase
        """
        self.amount += amount

    def decrease(self, amount: int) -> None:
        """decreases stock class attribute amountOfStock 

        Args:
            amount (int): amount to decrease
        """
        if self.amount - amount >= 0: self.amount -= amount
        else: print("Stock: Insufficient amount of stock to sell.")
