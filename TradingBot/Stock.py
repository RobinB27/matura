import yfinance as yf

from Util.Config import Config

import pandas as pd


class Stock:
    
    """
        defines the Stock class to be used by the portfolio, keeps track of amount of stock bought and pertinent information
        args: name
    """
    def __init__(self, name):
        
        self.name = str(name)
        self.amountOfStock = 0
        self.tickerObject = yf.Ticker(name)
        self.stockInfo = self.tickerObject.history(period ="max")
    
        # Throws exception message on invalid Ticker
        try: 
            self.tickerInfo = self.tickerObject.info
            pass
        except KeyError:
            raise ValueError("Unrecongnised ticker")
        
    
    def getStockPrice(self, mode: int = 0, dateStart: str ='0') -> int:
        """fetches stock prices, default mode is live prices, past mode has daily intevals
        Args: mode (-1 for past mode), start date('year-month-day')

        Args:
            mode (int, optional): live or past mode. Defaults to 0.
            dateStart (str, optional): _description_. date to fetch prices.

        Returns:
            _type_: int
        """
        if mode == 0:
            placeholder = yf.Ticker(self.name).info
            try:
                stockPrice = placeholder.get("currentPrice")
                print(stockPrice)
            except KeyError:
                print("Error: Market not open/Exception date")
            
            return stockPrice
        
        elif mode == -1:
            try:                
                closing_price = self.stockInfo.loc[dateStart, "Close"]
                if Config.debug():  
                    print(f"{self.name} price of {closing_price} on {dateStart}")
                
                return closing_price
            
            except KeyError:
                
                if Config.debug():  
                    print(f"Stock: exception date: {dateStart}")    
                return None
            
            
    def getStockPricesUntilDate(self, dateToCalculate):
        """fetches past stock prices for a period of time until a a given date
        date is included 
        Args: start date('year-month-day')

        Args:
            dateToCalculate (str): the last date of prices

        Returns:
            _type_: list -> int
        """
        try:
            historical_data = self.tickerObject.history(period="max")
            # Removes not a number rows (NaN rows)
            historical_data = historical_data.dropna()  
            historical_data = historical_data[historical_data.index <= dateToCalculate]            
            prices = historical_data['Close'].to_list()
            return prices

        except KeyError:
            if Config.debug():
                print(f"Stock: exception date: {dateToCalculate}")
            return {}
    
            
        
    def displayStockAmount(self):      
        """displays the stock class attribute amountOfStock 
        for debugging purposes
        """
        print(f"Number of {self.name} owned: {self.amountOfStock}")
        
        
    def increaseStockAmount(self, amount):
        """increases stock class attribute amountOfStock 

        Args:
            amount (int): amount to increase
        """
        self.amountOfStock += amount
        
        
    def decreaseStockAmount(self, amount):
        """decreases stock class attribute amountOfStock 

        Args:
            amount (int): amount to decrease
        """  
        if self.amountOfStock - amount >= 0:
            self.amountOfStock -= amount
        else:
            print("Stock: Insufficient amount of stock to sell.")
            