import yfinance as yf
class Stock:
    
    """
        defines the Stock class to be used by the portfolio, keeps track of amount of stock bought and pertinent information
    """
    
    def __init__(self, name):
        self.ticker = yf.Ticker(name)
        self.amountOfStock = 0
        self.infoTicker = self.ticker.info
        self.market_price = self.infoTicker['regularMarketPrice']
        self.previous_close_price = self.infoTicker['regularMarketPreviousClose']
        
    def displayStockAmount(self):
        
        print(f"Number of {self.ticker} owned: {self.amountOfStock}")