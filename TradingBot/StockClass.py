import yfinance as yf

class Stock:
    
    def __init__(self, name):
        
        #declares 
        self.ticker = yf.Ticker(name)
        self.amountOfStock = 0

        
        #
        self.infoTicker = self.ticker.info
        self.market_price = self.infoTicker['regularMarketPrice']
        self.previous_close_price = self.infoTicker['regularMarketPreviousClose']
        
    def displayStockAmount(self):
        print(f"Number of {self.ticker} owned: {self.amountOfStock}")