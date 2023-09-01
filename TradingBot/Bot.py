# This file contains the Bot class. This is where all other components come together into one whole (see other files). 
# The bot uses a specified trading strategy to trade over a time period given by the user.
# The users decides which stocks (see Stock.py) should be added to the bot's portfolio (see Portfolio.py). 
# The decisionmaking then decides day after day or time period by time period whether to buy/or sell a stock. This happens for each stock individually
# At the end of a trading day the bot logs the information (see FileLoggerTXT.py and FileLoggerJSON.py), where the results of a given run are stored
# The results can then be viewed by the graphing class (see graphing.py).

from datetime import datetime
import time

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
        # NOTE: is this property necessary or used anywhere? Would like to remove
        self.name = "trading bot"
        self.mode = mode

        self.startDate = startDate
        self.date = startDate

        # Keep these at None so testing if they're unassigned is straightforward
        self.portfolio: Portfolio = None
        self.timePeriod: int = None
        self.interval: int = None # in minutes
        self.amountOfIntervals: int = None

        self.decisionMaker = decisionMaking
        self.decisionMakerInstances = []
        self.fileLoggerTxt = FileLoggertxt()
        self.fileLoggerJSON = FileLoggerJSON()

    def initialise(self, funds: int, stocks: list[str], period: int, interval: int = None) -> None:
        """This method initializes the trading bot's portfolio, stock holdings
        and trading parameters.
        Prepares the bots decision-making and creates Log files

        Side Effects:
            - Initializes the bot's portfolio
            - Adds stocks to the portfolio
            - Sets the trading time period OR interval & repetions (depending on mode)
            - Creates a log file for text-based logging
            - Prepares decision-making strategies based on the selected mode and portfolio holdings

        Note:
            An initialisation method (this one or the non-CLI version) needs to be called before the startBot method
        """
        self.portfolio = Portfolio(funds)
        for stock in stocks: self.portfolio.addStock(stock)
        
        # Setup depending on mode
        if interval is None: self.timePeriod = period
        else: 
            self.interval = interval 
            self.amountOfIntervals = period

        # Check class type and populate Instances list
        decisionMakingType = self.decisionMaker.__class__
        for i in range(len(self.portfolio.stocksHeld)):
            self.decisionMakerInstances.append(decisionMakingType(self.mode))
        
        self.fileLoggerTxt.createLogFile()

    def initialiseCLI(self) -> None:
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
            An initialisation method (this one or the non-CLI version) needs to be called before the startBot method
        """
        funds = input("How many funds $$$ does the portfolio have? ")
        funds = int(funds)

        self.portfolio = Portfolio(funds)

        # NOTE: Maybe instead of giving a fixed number, let user add stocks until he types "EXIT" or something similar
        stockAmount = input("Number of stock to add to Portfolio: ")
        stockAmount = int(stockAmount)

        for i in range(stockAmount):
            newTicker = input("Ticker: ")

            self.portfolio.addStock(newTicker)
        if self.mode == -1:
            timePeriod = input("For how many days should the Bot trade? ")
            timePeriod = int(timePeriod)
            self.timePeriod = timePeriod

        self.fileLoggerTxt.createLogFile()

        # Check class type and populate Instances list
        decisionMakingType = self.decisionMaker.__class__
        for i in range(len(self.portfolio.stocksHeld)):
            self.decisionMakerInstances.append(decisionMakingType(self.mode))
            
        if self.mode == 0:
            self.interval = int(input("What interval will the bot be trading at (in minutes): "))
            self.amountOfIntervals = int(input("How often should the bot trade: "))

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
    
    def updatePortfolio(self) -> None:
        """
        Utility function to get Buy/sell/hold decisions from the DecisionMaking instances for all stocks and apply them to the portfolio.\n
        This is used on every iteration of the bot. Automatically updates FileLoggers.
        
        """
        for i in range(len(self.decisionMakerInstances)):
            decision = self.decisionMakerInstances[i].makeStockDecision(self.portfolio, self.portfolio.stocksHeld[i].ticker, self.mode, self.date, self.interval)

            if decision == 1:
                print(f"Bot:\t Buying stock: {self.portfolio.stocksHeld[i].ticker} on {self.date}")
                self.portfolio.buyStock(1, self.portfolio.stocksHeld[i].ticker, self.mode, self.date)
                self.fileLoggerTxt.snapshot(self.portfolio, self.mode, self.date)

            elif decision == -1:
                print(f"Bot:\t Selling stock: {self.portfolio.stocksHeld[i].ticker} on {self.date}")
                self.portfolio.sellStock(1, self.portfolio.stocksHeld[i].ticker, self.mode, self.date)
                self.fileLoggerTxt.snapshot(self.portfolio, self.mode, self.date)

            else:
                if Config.debug(): print(f"Bot:\t Ignoring stock: {self.portfolio.stocksHeld[i].ticker} on {self.date}")
            
            # Always update JSON log file, regardless of decision
            self.fileLoggerJSON.snapshot(self.portfolio, self.mode, self.date)

    def start(self) -> None:
        """Start the trading activities of the bot based on the specified mode and strategy

        This method initiates the trading activities of the bot by iterating through the specified
        time period, skipping weekends, and making stock trading decisions according to the bot's mode and decision-making strategy
        logs trading actions in JSON and TXT format, creates a value over time Graph and saves to output.
        """

        # Real time
        if self.mode == 0:
            # Main trading loop, custom interval
            for i in range(self.amountOfIntervals):
                # Exception date check
                while True:
                    self.date: str = datetime.now().strftime("%Y-%m-%d")
                    
                    if self.isExceptionDate():
                        print("Bot\t Exception date/stock market not open yet, retry in 10m")
                        time.sleep(600) # time in seconds
                        continue
                    else:
                        print("Bot:\t Currently valid trading hours, beginning trading.")
                        break        
                
                self.updatePortfolio()
                #   waiting until next schedueled interval
                if Config.debug():
                    print("going to sleep")
                time.sleep(self.interval * 60)
                
        # Historical data      
        elif self.mode == -1:
            # Main trading loop, fixed interval at 1d
            for i in range(self.timePeriod):
                # Exception date check
                if self.isExceptionDate(): continue
                else: self.updatePortfolio()

                # NOTE: datetimes
                self.date = self.portfolio.addDayToDate(self.date)
                if Config.debug():
                    print(f"Bot:\t Date updated to: {self.date}")

        # Output handling
        if Config.getParam("displayGraph"):
            if Config.debug():
                print("Bot:\t Creating graph")
            Graphing.plotValue(
                "logs/" + self.fileLoggerJSON.fileName, displayWindow=True)

        if Config.debug():
            print("Bot:\t closing cache")
