from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.MACDDecisionMaking import MACDDecisionMaking
from TradingBot.FileLoggerJSON import FileLoggerJSON
from TradingBot.FileLoggertxt import FileLoggertxt
import datetime

class Bot:
    def __init__(self, startDate, mode = 0):
        self.name = "trading bot"
        self.mode = mode
        self.startDate = startDate
        self. portfolio = 0
        self.date = ""
        self.timePeriod = 0
        self.decisionMaker = MACDDecisionMaking(mode)
        #add in a self.date class attribute such that the bot can keep track of what date it is
        
    def initiating(self):
        fundsForPortfolio = input("How many funds $$$ does the portfolio have? ")
        fundsForPortfolio = int(fundsForPortfolio)
                
        self.portfolio = Portfolio(fundsForPortfolio)
        
        amountOfStocks = input("Amount of stock to add: ")
        amountOfStocks = int(amountOfStocks)
        
        for i in range(amountOfStocks):
            nameOfTickerToAdd = input("Ticker: ")
            
            self.portfolio.addStock(nameOfTickerToAdd)
        
        timePeriod = input("For how many days should the Bot trade? ")
        timePeriod = int(timePeriod)
        self.timePeriod = timePeriod
    
    def startBot(self):
        if self.mode == -1:
            
            for i in range(self.timePeriod):
                print(f"{self.date}")
                stockName = self.portfolio
                
                #DOES NOT WORK YET
                decisions = map(self.decisionMaker.makeStockDecision(self.portfolio, stock.name, self.mode, self.date), self.portfolio.stocksHeld)

                for decision, stock in zip(decisions, self.portfolio.stocksHeld):
                    if decision == 1:
                        self.portfolio.buyStock(10, stock.name, self.mode, self.date)
                        print(f"Buying stock: {stock.name}")
                    elif decision == 0:
                        self.portfolio.sellStock(10, stock.name, self.mode, self.date)
                        print(f"Selling stock: {stock.name}")
                    else:
                        print(f"Ignoring stock: {stock.name}")
        
    #remember the map function to iterate over all stocks held and decide if you should sell them
    
    
    