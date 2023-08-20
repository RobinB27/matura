import yfinance as yf

from Util.Config import Config


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
    
        # Throws useful exception message on invalid Ticker
        try: 
            self.tickerInfo = self.tickerObject.info
            pass
        except KeyError:
            raise ValueError("Unrecongnised ticker")
        
    
    #at some point has to be changed to utilise the download method of yf more precisely (time period)
    def getStockPrice(self, mode: int = 0, dateStart='0'):
        """
        fetches stock prices, default mode is live prices, past mode (daily intevals)
        Args: mode (-1 for past mode), start date('year-month-day'), end date
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
        try:
            historical_data = self.tickerObject.history(period="max")
            historical_data = historical_data.dropna()  # Remove NaN rows
            historical_data = historical_data[historical_data.index <= dateToCalculate]            
            prices = historical_data['Close'].to_dict()
            return prices

        except KeyError:
            if Config.debug():
                print(f"Stock: exception date: {dateToCalculate}")
            return {}
            
        
    def displayStockAmount(self):      
        print(f"Number of {self.name} owned: {self.amountOfStock}")
        
        
    def increaseStockAmount(self, amount):     
        self.amountOfStock += amount
        
        
    def decreaseStockAmount(self, amount):   
        if self.amountOfStock - amount >= 0:
            self.amountOfStock -= amount
        else:
            print("Stock: Insufficient amount of stock to sell.")
            