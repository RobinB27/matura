from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.MACDDecisionMaking import MACDDecisionMaking
from TradingBot.FileLoggers.FileLoggerJSON import FileLoggerJSON
from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt
from datetime import  datetime, timedelta, date
from diskcache import Cache

#in time period bot skipps weekends but counts them as a day of the time period

class Bot:
    def __init__(self, startDate: str="", mode = 0):
        self.name = "trading bot"
        self.mode = mode
        
        self.startDate = startDate
        self.date = startDate
        
        self.portfolio = 0
        self.timePeriod = 0
        
        self.decisionMaker = MACDDecisionMaking(mode)
        self.fileLoggerTxt = FileLoggertxt()
        self.fileLoggerJSON = FileLoggerJSON()
        
        self.cache = Cache("./TradingBot/FinancialCalculators/CacheSMA")

    
        
        
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
        if self.mode == 0:
            pass
        
        if self.mode == -1:
            
            #have to implement checks for valid dates
            
            #checks for valid date: 
            
            for i in range(self.timePeriod):
                
                print(f"Bot: Trading day: {self.date}")
                
                weekendCheckDatetime = datetime.strptime(self.date, "%Y-%m-%d")
                exceptionCheckDate = self.portfolio.addDayToDate(self.date)
                
                if weekendCheckDatetime.isoweekday() > 5:
                    print(f"Bot: weekend: {self.date}")
                    self.date = self.portfolio.addDayToDate(self.date)
                    continue
                
                print("Bot: downloading Stock price for Exception date check")
                if self.portfolio.stocksHeld[0].getStockPrice(-1, self.date, exceptionCheckDate) is None:
                    print(f"Bot: exception date: {self.date}")
                    self.date = self.portfolio.addDayToDate(self.date)
                    continue
                                
                for stock in self.portfolio.stocksHeld:
                    decision = self.decisionMaker.makeStockDecision(self.portfolio, stock.name, self.mode, self.date)

                    if decision == 1:
                        print(f"Bot: Buying stock: {stock.name}")
                        self.portfolio.buyStock(1, stock.name, self.mode, self.date)
                    elif decision == 0:
                        print(f"Bot: Selling stock: {stock.name}")
                        self.portfolio.sellStock(1, stock.name, self.mode, self.date)
                    else:
                        print(f"Bot: Ignoring stock: {stock.name}")
                        
                self.fileLoggerTxt.snapshot(self.portfolio, self.mode, self.date)
                
                self.date = self.portfolio.addDayToDate(self.date)
                print(self.date)

            print("Bot: Closing cache")
            self.cache.close()
        
    
    
    