import sys
sys.path.append('/path/to/TradingBot')
from TradingBot.StockClass import Stock
class Portfolio:
    """
    defines the portfolio class
    """
    def __init__(self, amount):
        self.funds = amount
        self.stocksHeld = []
    
   
    def addStock(self, ticker):
        """
        adds a stock to the portfolio
        """
        self.stocksHeld.append(Stock(ticker))
    
    def buyStock(self, amount: int):
        """
            buys the stock if the funds are available
        """
        if self.funds - (self.market_price * amount) >= 0:
            self.amountOfStock += amount
            self.Funds -= amount * self.market_price
        
    
    def sellStock(self, amount: int):
        if self.amountOfStock - amount >= 0:
            self.amountOfStock -= amount    
        
p1 = Portfolio(1000)



            