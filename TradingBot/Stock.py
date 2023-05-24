import yfinance as yf
class Stock:
    
    """
        defines the Stock class to be used by the portfolio, keeps track of amount of stock bought and pertinent information
    """
    
    def __init__(self, name):
        
        self.name = name
            
        self.amountOfStock = 0
    
        try: 
            self.tickerInfo = yf.Ticker(name).info
        except KeyError:
            raise ValueError("Unrecongnised ticker")
    
    def getCurrentStockPrice(self):
        placeholder = yf.Ticker(self.name).info
        stockPrice = placeholder.get("currentPrice")
        return stockPrice
        
        
    def displayStockAmount(self):
        
        print(f"Number of {self.name} owned: {self.amountOfStock}")
        
    def increaseStockAmount(self, amount):
        self.amountOfStock += amount
        
    def decreaseStockAmount(self, amount):
        if self.amountOfStock - amount != 0:
            self.amountOfStock -= amount
        else:
            return 0