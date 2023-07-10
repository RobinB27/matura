from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.MACDDecisionMaking import MACDDecisionMaking
from TradingBot.FileLoggers.FileLoggerJSON import FileLoggerJSON
from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt
import datetime

class Bot:
    def __init__(self, startDate, mode = 0):
        self.name = "trading bot"
        self.mode = mode
        self.startDate = startDate
        self. portfolio = 0
        self.date = startDate
        self.timePeriod = 0
        self.decisionMaker = MACDDecisionMaking(mode)
        self.fileLoggerTxt = FileLoggertxt()
        self.fileLoggerJSON = FileLoggerJSON()
        
        #add in a self.date class attribute such that the bot can keep track of what date it is
        
    def initiating(self):
        fundsForPortfolio = input("How many funds $$$ does the portfolio have? ")
        fundsForPortfolio = int(fundsForPortfolio)
                
        self.portfolio = Portfolio(fundsForPortfolio)
        
        amountOfStocks = input("Number of stock to add to Portfolio: ")
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
                                
                for stock in self.portfolio.stocksHeld:
                    decision = self.decisionMaker.makeStockDecision(self.portfolio, stock.name, self.mode, self.date)

                    if decision == 1:
                        self.portfolio.buyStock(10, stock.name, self.mode, self.date)
                        print(f"Buying stock: {stock.name}")
                    elif decision == 0:
                        self.portfolio.sellStock(10, stock.name, self.mode, self.date)
                        print(f"Selling stock: {stock.name}")
                    else:
                        print(f"Ignoring stock: {stock.name}")
                        
                self.fileLoggerTxt.snapshot(self.portfolio, self.mode, self.date)
                
                self.date = self.portfolio.addDayToDate(self.date)
                print(self.date)
        
    
    
    