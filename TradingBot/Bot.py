from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.SimpleSentimentDM import SimpleSentimentDM
from TradingBot.MACDDecisionMaking import MACDDecisionMaking
from TradingBot.FileLoggers.FileLoggerJSON import FileLoggerJSON
from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt
from datetime import  datetime, timedelta, date
from diskcache import Cache

from Util.Config import Config

#in time period bot skipps weekends but counts them as a day of the time period
#so to get full trading week timePeriod has to equal 7

class Bot:
    """Trading bot class that makes decisions based on a specified decision-making
    The bot operates within a given time period, trading stocks in a portfolio and logging its actions.
    
    Attributes:
        name (str): name of trading bot
        mode (int): live mode 0, past mode -1
        startDate (str): start date for trading: format "YYYY-MM-DD"
        date (str): current trading date: format "YYYY-MM-DD".
        portfolio (Portfolio): instance of Portfolio class containing stocks and funds
        timePeriod (int): trading period in days
        decisionMaker (DecisionMakingStrategy): instance of a decision-making used by the bot.
        fileLoggerTxt (FileLoggertxt): instance of the FileLoggertxt class for text-based logging
        fileLoggerJSON (FileLoggerJSON): instance of the FileLoggerJSON class for JSON-based logging
    Methods:
        initiating(self): initialize the bot, set up the portfolio, and prepare decision-making strategies
        startBot(self): start the bot's trading activities based on the specified mode and strategy

    Note:
        The bot operates in two modes: live (0) and past  (-1). 
    """
    def __init__(self, decisionMaking, startDate: str="", mode = 0):
        """ Initializes a trading bot with a decision-making strategy, start date, trading mode

        Args:
            decisionMaking (DecisionMakingStrategy): instance of the decision-making strategy used by the bot
            startDate (str, optional): start date for trading in "YYYY-MM-DD" format: Defaults to an empty string.
            mode (int, optional):  trading mode: 0 for live, -1 for past. Defaults to 0.
        """

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
        """This method initializes the trading bot's portfolio, stock holdings
        and trading parameters. Prompts the user for input regarding funds, stocks, and the trading period
        Prepares the bots decision-making and creates Log files

        Side Effects:
            - Initializes the bot's portfolio with user-provided funds
            - Adds stocks to the portfolio based on user input
            - Sets the trading time period
            - Creates a log file for text-based logging
            - Prepares decision-making strategies based on the selected mode and portfolio holdings
            
        Note:
            This method needs to be called before the startBot method
        """
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
        
        
        self.DecisionMakerList = []
        
        if isinstance(self.decisionMaker, MACDDecisionMaking):
            for i in range(len(self.portfolio.stocksHeld)):
                self.DecisionMakerList.append(MACDDecisionMaking(self.mode))
                
        elif isinstance(self.decisionMaker, SimpleSentimentDM):
            for i in range(len(self.portfolio.stocksHeld)):
                self.DecisionMakerList.append(SimpleSentimentDM(self.mode))
            
                
        
    
    def startBot(self):
        """Start the trading activities of the bot based on the specified mode and strategy

        This method initiates the trading activities of the bot by iterating through the specified
        time period, skipping weekends, and making stock trading decisions according to the bot's mode and decision-making strategy
        logs trading actions in JSON and TXT format
        """
    
        if self.mode == 0:
            pass
    
        if self.mode == -1:            
        
            for i in range(self.timePeriod):
                
                if Config.debug():
                    print(f"Bot: Trading day: {self.date}")
            
                weekendCheckDatetime = datetime.strptime(self.date, "%Y-%m-%d")
            
                if weekendCheckDatetime.isoweekday() > 5:
                    if Config.debug():
                        print(f"Bot: weekend: {self.date}")
                    self.date = self.portfolio.addDayToDate(self.date)
                    continue
            
                if Config.debug():
                    print("Bot: downloading Stock price for Exception date check")
                if self.portfolio.stocksHeld[0].getStockPrice(-1, self.date) is None:
                    if Config.debug():
                        print(f"Bot: exception date: {self.date}")
                    self.date = self.portfolio.addDayToDate(self.date)
                    continue
                
                for i in range(len(self.DecisionMakerList)):
                    decision = self.DecisionMakerList[i].makeStockDecision(self.portfolio, self.portfolio.stocksHeld[i].name, self.mode, self.date)
                    
                #for stock in self.portfolio.stocksHeld:
                    #decision = self.decisionMaker.makeStockDecision(self.portfolio, stock.name, self.mode, self.date)

                    if decision == 1:
                        
                        print(f"Bot: Buying stock: {self.portfolio.stocksHeld[i].name} on {self.date}")
                        self.portfolio.buyStock(1, self.portfolio.stocksHeld[i].name, self.mode, self.date)
                        self.fileLoggerTxt.snapshot(self.portfolio, self.mode, self.date)

                    elif decision == -1:
                        
                        print(f"Bot: Selling stock: {self.portfolio.stocksHeld[i].name} on {self.date}")
                        self.portfolio.sellStock(1, self.portfolio.stocksHeld[i].name, self.mode, self.date)
                        self.fileLoggerTxt.snapshot(self.portfolio, self.mode, self.date)

                    else:
                        if Config.debug():
                            print(f"Bot: Ignoring stock: {self.portfolio.stocksHeld[i].name} on {self.date}")
                    
                #self.fileLoggerTxt.snapshot(self.portfolio, self.mode, self.date)
                self.fileLoggerJSON.snapshot(self.portfolio, self.mode, self.date)
            
                self.date = self.portfolio.addDayToDate(self.date)
                if Config.debug():
                    print(self.date)
                   
        if Config.debug():            
            print("closing cache")
