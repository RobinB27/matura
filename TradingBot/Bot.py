# This file contains the Bot class. This is where all other components come together into one whole (see other files). 
# The bot uses a specified trading strategy to trade over a time period given by the user.
# The users decides which stocks (see Stock.py) should be added to the bot's portfolio (see Portfolio.py). 
# The decisionmaking then decides day after day or time period by time period whether to buy/or sell a stock. This happens for each stock individually
# At the end of a trading day the bot logs the information (see FileLoggerTXT.py and FileLoggerJSON.py), where the results of a given run are stored
# The results can then be viewed by the graphing class (see graphing.py).

from datetime import datetime
import pytz
import time

from TradingBot.Stock import Stock
from TradingBot.Portfolio import Portfolio
from TradingBot.FileLoggers.FileLoggerJSON import FileLoggerJSON
from TradingBot.FileLoggers.FileLoggertxt import FileLoggertxt

from Util.Graphing import Graphing
from Util.Config import Config


class Bot:
    """Trading bot class that makes decisions based on a specified decision-making (trading strategy)
    The bot operates within a given time period, trading stocks in a portfolio and logging its actions.

    Attributes:
        name (str): name of trading bot NOTE: is this needed? Remove if not
        mode (int): live mode 0, past mode -1
        startDate (str): start date for trading: format "YYYY-MM-DD" NOTE: change to dateTime
        date (str): current trading date: format "YYYY-MM-DD".
        portfolio (Portfolio): instance of Portfolio class containing stocks and funds
        timePeriod (int): trading period in days, including weekends where no trades happen. NOTE: Needs to be updated to allow for intraday timeperiods later
        decisionMaker (DecisionMakingStrategy): instance of a decision-making used by the bot.
        fileLoggerTxt (FileLoggertxt): instance of the FileLoggertxt class for text-based logging
        fileLoggerJSON (FileLoggerJSON): instance of the FileLoggerJSON class for JSON-based logging

    Methods:
        initiating(self): initialize the bot, set up the portfolio, and prepare decision-making strategies
        startBot(self): start the bot's trading activities based on the specified mode and strategy

    Note:
        The bot operates in two modes: live (0) and past (-1). 
    """

    def __init__(self, decisionMaking, startDate: str = "", mode: int = 0) -> None:
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

        self.portfolio = None
        self.timePeriod = 0
        self.interval = 0 #given in minutes
        self.amountOfIntervals = 0

        self.decisionMaker = decisionMaking
        self.fileLoggerTxt = FileLoggertxt()
        self.fileLoggerJSON = FileLoggerJSON()

        # NOTE: we also need a way later on to create bots with code instead of command line, for automated tests
    def initialiseCLI(self):
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

        # NOTE: Maybe instead of giving a fixed number, let user add stocks until he types "EXIT" or something similar
        amountOfStocks = input("Number of stock to add to Portfolio: ")
        amountOfStocks = int(amountOfStocks)

        for i in range(amountOfStocks):
            nameOfTickerToAdd = input("Ticker: ")

            self.portfolio.addStock(nameOfTickerToAdd)
        if self.mode == -1:
            timePeriod = input("For how many days should the Bot trade? ")
            timePeriod = int(timePeriod)
            self.timePeriod = timePeriod

        self.fileLoggerTxt.createLogFile()

        self.decisionMakerInstances = []

        # Check class type and populate Instances list
        decisionMakingType = self.decisionMaker.__class__
        for i in range(len(self.portfolio.stocksHeld)):
            self.decisionMakerInstances.append(decisionMakingType(self.mode))
            
        if self.mode == 0:
            self.interval = int(input("What interval will the bot be trading (in minutes): "))
            self.amountOfIntervals = int(input("What amount of interval will the bot be trading: "))

    def isExceptionDate(self) -> bool:
        """Utility function to check whether a date is either weekend or exception Date.

        Returns:
            bool: True if exception date else False
        """
        if Config.debug():
            print(f"Bot:\t Trading day: {self.date}")

        weekendCheckDatetime = datetime.strptime(self.date, "%Y-%m-%d")
        
        if weekendCheckDatetime.isoweekday() > 5:
            if Config.debug():
                print(f"Bot:\t weekend: {self.date}")
            self.date = self.portfolio.addDayToDate(self.date)
            return True
        # NOTE: removed a console message here to improve code legibility, re-add if you think it's necessary
        if self.mode == 0:
            if self.portfolio.stocksHeld[0].getPrice() is None:
                if Config.debug():
                    print(f"Bot:\t exception date: {self.date}")
                self.date = self.portfolio.addDayToDate(self.date)
                return True
        if self.mode == -1:
            
            if self.portfolio.stocksHeld[0].getPrice(-1, self.date) is None:
                if Config.debug():
                    print(f"Bot:\t exception date: {self.date}")
                self.date = self.portfolio.addDayToDate(self.date)
                return True
        else:
            return False

    def start(self) -> None:
        """Start the trading activities of the bot based on the specified mode and strategy

        This method initiates the trading activities of the bot by iterating through the specified
        time period, skipping weekends, and making stock trading decisions according to the bot's mode and decision-making strategy
        logs trading actions in JSON and TXT format, creates a value over time Graph and saves to output.
        """

        if self.mode == 0:
            # Main trading loop
            for i in range(self.amountOfIntervals):
                while True:
                    self.date = datetime.now()
                    self.date = self.date.strftime("%Y-%m-%d")
                    
                    if self.isExceptionDate():
                        print("exception date/stock market not open yet, going to sleep for 10 minutes before trying agian")
                        time.sleep(600) # time in minutes for
                        continue
                    else:
                        print("valid trading hours")
                        break        
                
                # stock decisions
                for i in range(len(self.decisionMakerInstances)):
                        decision = self.decisionMakerInstances[i].makeStockDecision(
                            self.portfolio, self.portfolio.stocksHeld[i].ticker, self.mode, self.date, self.interval)
                    
                        # decision execution / logging 
                        if decision == 1:
                            print(f"Bot:\t Buying stock: {self.portfolio.stocksHeld[i].ticker} on {self.date}")
                            self.portfolio.buyStock(
                                1, self.portfolio.stocksHeld[i].ticker, self.mode, self.date)
                            self.fileLoggerTxt.snapshot(
                                self.portfolio, self.mode, self.date)

                        elif decision == -1:
                            print(f"Bot:\t Selling stock: {self.portfolio.stocksHeld[i].ticker} on {self.date}")
                            self.portfolio.sellStock(
                                1, self.portfolio.stocksHeld[i].ticker, self.mode, self.date)
                            self.fileLoggerTxt.snapshot(
                            self.portfolio, self.mode, self.date)

                        else:
                            if Config.debug():
                                print(f"Bot:\t Ignoring stock: {self.portfolio.stocksHeld[i].ticker} on {self.date}")
                
                #   waiting until next schedueled interval
                time.sleep(self.interval * 60)
                
                         
                
        elif self.mode == -1:

            # Main trading loop
            for i in range(self.timePeriod):

                if self.isExceptionDate():
                    continue

                # Seperate Decision Making instance for each stock in portfolio
                for i in range(len(self.decisionMakerInstances)):
                    decision = self.decisionMakerInstances[i].makeStockDecision(
                        self.portfolio, self.portfolio.stocksHeld[i].ticker, self.mode, self.date)

                    if decision == 1:
                        print(f"Bot:\t Buying stock: {self.portfolio.stocksHeld[i].ticker} on {self.date}")
                        self.portfolio.buyStock(
                            1, self.portfolio.stocksHeld[i].ticker, self.mode, self.date)
                        self.fileLoggerTxt.snapshot(
                            self.portfolio, self.mode, self.date)

                    elif decision == -1:
                        print(f"Bot:\t Selling stock: {self.portfolio.stocksHeld[i].ticker} on {self.date}")
                        self.portfolio.sellStock(
                            1, self.portfolio.stocksHeld[i].ticker, self.mode, self.date)
                        self.fileLoggerTxt.snapshot(
                            self.portfolio, self.mode, self.date)

                    else:
                        if Config.debug():
                            print(f"Bot:\t Ignoring stock: {self.portfolio.stocksHeld[i].ticker} on {self.date}")

                self.fileLoggerJSON.snapshot(
                    self.portfolio, self.mode, self.date)

                # NOTE: datetimes
                self.date = self.portfolio.addDayToDate(self.date)
                if Config.debug():
                    print(f"Bot:\t Date updated to: {self.date}")

        if Config.getParam("displayGraph"):
            if Config.debug():
                print("Bot:\t Creating graph")
            Graphing.plotValue(
                "logs/" + self.fileLoggerJSON.fileName, displayWindow=True)

        if Config.debug():
            print("Bot:\t closing cache")
