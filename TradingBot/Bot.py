from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.MACDDecisionMaking import MACDDecisionMaking
from TradingBot.FileLoggers.FileLoggerJSON import FileLoggerJSON
from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt
from datetime import  datetime, timedelta, date
from diskcache import Cache

from Util.Config import Config



#in time period bot skipps weekends but counts them as a day of the time period
#so to get full trading week timePeriod has to equal 7

class Bot:
    def __init__(self, decisionMaking, startDate: str="", mode = 0):
        self.name = "trading bot"
        self.mode = mode
        
        self.startDate = startDate
        self.date = startDate
        
        self.portfolio = 0
        self.timePeriod = 0
        
        self.decisionMaker = decisionMaking
        self.fileLoggerTxt = FileLoggertxt()
        self.fileLoggerJSON = FileLoggerJSON()
                        
        
        
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
        
        self.fileLoggerTxt.createLogFile()
        
        if isinstance(self.decisionMaker, MACDDecisionMaking):
            self.MACDDecisionMakerList = []
            
            for i in range(len(self.portfolio.stocksHeld)):
                self.MACDDecisionMakerList.append(MACDDecisionMaking(self.mode))
                
        
    
    def startBot(self):
        if isinstance(self.decisionMaker, MACDDecisionMaking):
            if self.mode == 0:
                pass
        
            if self.mode == -1:            
            
                for i in range(self.timePeriod):
                    
                    if Config.debug():
                        print(f"Bot: Trading day: {self.date}")
                
                    weekendCheckDatetime = datetime.strptime(self.date, "%Y-%m-%d")
                    exceptionCheckDate = self.portfolio.addDayToDate(self.date)
                
                    if weekendCheckDatetime.isoweekday() > 5:
                        if Config.debug():
                            print(f"Bot: weekend: {self.date}")
                        self.date = self.portfolio.addDayToDate(self.date)
                        continue
                
                    if Config.debug():
                        print("Bot: downloading Stock price for Exception date check")
                    if self.portfolio.stocksHeld[0].getStockPrice(-1, self.date, exceptionCheckDate) is None:
                        if Config.debug():
                            print(f"Bot: exception date: {self.date}")
                        self.date = self.portfolio.addDayToDate(self.date)
                        continue
                    
                    for i in range(len(self.MACDDecisionMakerList)):
                        decision = self.MACDDecisionMakerList[i].makeStockDecision(self.portfolio, self.portfolio.stocksHeld[i].name, self.mode, self.date)
                        
                    #for stock in self.portfolio.stocksHeld:
                        #decision = self.decisionMaker.makeStockDecision(self.portfolio, stock.name, self.mode, self.date)

                        if decision == 1:
                            
                            print(f"Bot: Buying stock: {self.portfolio.stocksHeld[i].name}")
                            self.portfolio.buyStock(1, self.portfolio.stocksHeld[i].name, self.mode, self.date)
                        elif decision == 0:
                            
                            print(f"Bot: Selling stock: {self.portfolio.stocksHeld[i].name}")
                            self.portfolio.sellStock(1, self.portfolio.stocksHeld[i].name, self.mode, self.date)
                        else:
                            if Config.debug():
                                print(f"Bot: Ignoring stock: {self.portfolio.stocksHeld[i].name}")
                        
                    self.fileLoggerTxt.snapshot(self.portfolio, self.mode, self.date)
                    #self.fileLoggerJSON.snapshot(self.portfolio, self.mode, self.date)
                
                    self.date = self.portfolio.addDayToDate(self.date)
                    if Config.debug():
                        print(self.date)
