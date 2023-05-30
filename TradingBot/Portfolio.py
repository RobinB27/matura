from TradingBot.Stock import Stock
class Portfolio:
    """
    defines the portfolio class
    """
    def __init__(self, fundsAmount):
        self.funds = fundsAmount
        self.stockIdentifier = 0
        self.stocksHeld = {}
    
   
    def addStock(self, ticker):
        """
        adds a stock to the portfolio identifying them in order that they were added with 1,2,3 etc
        """
        try:
            
            
            self.stocksHeld [self.stockIdentifier] = Stock(ticker)
            self.stockIdentifier += 1
            
        except KeyError:
            raise ValueError("Unrecongnised ticker")
    
    def buyStock(self, amount: int, nameOfTicker: Stock):
        """
            buys the stock if the funds are available
        """ 
        try:
            for i in self.stocksHeld:
                if i == nameOfTicker:
                    self.stocksHeld[i].getCurrentStockPrice()
                
        except KeyError:
            raise ValueError("Unrecongnised ticker")
        
    def sellStock(self):
        pass
    
    def showStocksHeld(self):
        for i in self.stocksHeld:
            print(f"{self.stocksHeld[i]}")
        