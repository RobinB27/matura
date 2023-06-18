import yfinance as yf
class Stock:
    
    """
        defines the Stock class to be used by the portfolio, keeps track of amount of stock bought and pertinent information
        args: name
    """
    def __init__(self, name):
        
        self.name = name
        self.amountOfStock = 0
    
        # Throws useful exception message on invalid Ticker
        try: self.tickerInfo = yf.Ticker(self.name).info
        except KeyError:
            raise ValueError("Unrecongnised ticker")
        
    
    def getStockPrice(self, mode: int = 0, dateStart='0', dateEnd='0'):
        """
        fetches stock prices, default mode is live prices, past mode (daily intevals)
        Args: mode (-1 for past mode), start date('year-month-day'), end date
        """
        if mode == 0:
            placeholder = yf.Ticker(self.name).info
            stockPrice = placeholder.get("currentPrice")
            print(stockPrice)
            return stockPrice
        elif mode == -1:
            try:
                stockHistorical = yf.download(self.name, start=dateStart, end=dateEnd)
                
                closing_price = stockHistorical.loc[dateStart, "Close"]
                return closing_price
            except KeyError:
                print("No stock price available for the specified date range.")
                return None
            
        
    def displayStockAmount(self):      
        print(f"Number of {self.name} owned: {self.amountOfStock}")
        
        
    def increaseStockAmount(self, amount):     
        self.amountOfStock += amount
        
        
    def decreaseStockAmount(self, amount):   
        if self.amountOfStock - amount >= 0:
            self.amountOfStock -= amount
        else:
            print("Insufficient amount of stock to sell.")
            