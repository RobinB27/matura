from TradingBot.Stock import Stock
class Portfolio:
    """
    defines the portfolio class
    params: fundsAmount, name
    """
    def __init__(self, fundsAmount, name):
        
        self.name = name
        self.funds = fundsAmount
        self.stocksHeld = [] #could be optimised with a dict
       
    
   
    def addStock(self, ticker: str):
        """
        adds a stock to the portfolio identifying them in order that they were added with 1,2,3 etc
        params: ticker
        """
        try:
            
            self.stocksHeld.append(Stock(ticker))
            
        except KeyError:
            raise ValueError("Unrecongnised ticker")
                
                 
    def buyStock(self, amount: int, nameOfTicker: str):
        """
        buys the stock if the funds are available
        params: amount, nameOfTicker
        """ 
        try:
            for stock in self.stocksHeld:
                #checks if the given stock is a stock held by the portfolio
                if stock.name == nameOfTicker:
                    currentPrice = stock.getCurrentStockPrice()
                    totalCost = currentPrice * amount
                
                    #checks if there are enough funds to buy the stock & buys it
                    if totalCost <= self.funds:
                        self.funds -= totalCost
                        stock.increaseStockAmount(amount)
                        print(f"Bought {amount} shares of {nameOfTicker} at ${currentPrice} per share.")
                    else:
                        print("Insufficient funds to buy the stock.")
            
        except KeyError:
            raise ValueError("Unrecongnised ticker")
        
    def sellStock(self, amount: int, nameOfTicker: str):
        """
        sells the stock if the shares are available
        params: amount, nameOfTicker
        """ 
        try:
            for stock in self.stocksHeld:
                #checks if the given stock is a stock held by the portfolio
                if stock.name == nameOfTicker:
                    currentPrice = stock.getCurrentStockPrice()
                    totalPrice = currentPrice * amount
                    
                    #checks if there is enough of a given stock to sell & sells it
                    if stock.amountOfStock >= amount:
                        self.funds += totalPrice
                        stock.decreaseStockAmount(amount)
                        print(f"Sold {amount} shares of {nameOfTicker} at ${currentPrice} per share.")

                
            
        except KeyError:
            raise ValueError("Unrecongnised ticker")
    
    def showStocksHeld(self):
        for stock in self.stocksHeld:
            print(stock.name)
            
    def showFundsAvailable(self):
        print(f"Funds inside portfolio: \"{self.name}\" are ${self.funds}")
    
    def findStock(self, nameOfTicker: str):
        for stock in self.stocksHeld:
            if stock.name == nameOfTicker:
                return stock
            else:
                return -1