# This class implements several methods used for evaluating the viability of a trading strategy and for comparing strategies
from datetime import datetime, timedelta
import random, pathlib, os

from TradingBot.Bot import Bot
from TradingBot.Stock import Stock
from TradingBot.TemplateDM import TemplateDM
from TradingBot.FileLoggers.FileLoggerJSON import FileLoggerJSON
from TradingBot.BuyAndHoldDM import BuyAndHoldDM
from TradingBot.SimpleSentimentDM import SimpleSentimentDM
from TradingBot.AvgSentimentDM import AvgSentimentDM
from TradingBot.MACDDM import MACDDM

from Util.Graphing import Graphing
from Util.Config import Config

# As described in https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
class DateException(Exception): pass

class Testing:
    # These are constants and should NOT be changed
    maxDate = datetime(2020, 6, 11)
    # Technically goes back to 14 Feb 2009, but data amount stabilises in 2011
    minDate = datetime(2011, 1, 1)
    dateDelta = maxDate - minDate
    
    # As seen on 10/09/2023
    # from: https://www.nasdaq.com/market-activity/stocks/screener
    Nasdaq200B = ["AAPL", "MSFT", "GOOG", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "AVGO", "ADBE", "ASML", "COST", "PEP", "CSCO"]
    
    StockObjs = {}
    
    def CLI() -> None:
        """
        The CLI method to use the testing tool from the command line.\n
        This is used in the main function of the programme.
        """
        
        stratTable = {
            "0": None,
            "1": SimpleSentimentDM,
            "2": AvgSentimentDM,
            "3": MACDDM,
            "4": BuyAndHoldDM
        }
        
        # Get iterations
        print("Please select the amount of bot runs for the testing cycle")
        iterations = int(input("Runs:\t"))
        if iterations < 1: raise SyntaxError("Bot run count can't be below 0.")
        
        # Get starting funds
        print("Please select the bots starting funds.")
        funds = int(input("Funds: "))
        if funds < 0: raise SyntaxError("Funds can't be negative.")
        
        # Get first strategy
        print("Please select a trading strategy:\n(1) Simple Sentiment Strategy\n(2) Average Sentiment Strategy\n(3) MACD Strategy\n(4) Buy and Hold Strategy")
        strat1: int = int(input("Strategy: "))
        if strat1 < 1 or strat1 > 4: raise SyntaxError("Invalid argument passed. Please enter either 1, 2 or 3")
        strat1: object = stratTable[str(strat1)]
        
        # Get second strategy or disable
        print("Please select a second trading strategy:\n(0) No second strategy\n(1) Simple Sentiment Strategy\n(2) Average Sentiment Strategy\n(3) MACD Strategy\n(4) Buy and Hold Strategy")
        strat2: int = int(input("Strategy: "))
        if strat2 < 0 or strat2 > 4: raise SyntaxError("Invalid argument passed. Please enter either 0, 1, 2 or 3")
        strat2: object = stratTable[str(strat2)]
        
        # Get start date
        print("Please select a starting date in format DD-MM-YYYY")
        print("\tMaximum date: 11-06-2020\n\tMinimum date: 01-01-2011")
        startDate: str = str(input("Date:\t"))
        # Raises error if format is incorrect
        startDate: datetime = datetime.strptime(startDate, "%d-%m-%Y")
        
        # Get period
        print("Please enter the minimum trading duration (in days) for the test runs.")
        minDur = int(input("Min:\t"))
        if minDur < 1: raise SyntaxError("Minimum trading duration can't be below 1 day.")
        
        print("Please enter the maximum trading duration (in days) for the test runs.")
        maxDur = int(input("Max\t"))
        if maxDur < minDur: raise SyntaxError("Maximum trading duration can't be below minimum duration.")
        if maxDur == minDur: print("Minimum and maximum are equal, trading duration set as constant.")
        
        # Define stock list
        print("Please enter the Number of stocks for the porfolio. Enter 0 to randomize.")
        stockLen: int = int(input("Length: "))
        if stockLen < 0: raise SyntaxError("Stock list length can't be smaller than 0.")
        
        stockList = None
        if stockLen != 0:
            stockList = []
            for i in range(stockLen):
                print("Please enter a stock ticker (e.g. TSLA) to add to the portfolio")
                ticker = str(input("Ticker: "))
                stockList.append(ticker)
        
        periodLimits: tuple = (minDur, maxDur)
        if maxDur == minDur: periodLimits = maxDur
        
        print("Setup complete")
        
        # Select optimal testing function depending on input
        if strat2 == None:
            Testing.testMultiple(iterations, strat1, strat2, funds, startDate, stockList, periodLimits)
        else:
            Testing.compareDMs(iterations, strat1, strat2, funds, startDate, stockList, periodLimits)
                
    
    # single run
    def testSingle(Strategy: TemplateDM, funds: int, startDate: datetime, stockList: list[Stock], period: int, customPrefix: str = None, customFolder: str = None) -> dict:
        """Does a single test run with the specified parameters and returns the produced log

        Args:
            Strategy (TemplateDM): Valid DecisionMaking class which should be used
            startDate (datetime): Date at which trading should start. Must be after 1st January 2011.
            funds (int): Initial portfolio funds
            stockList (list[Stock]): List of stocks to add to Portfolio
            period (int): Amount of days for which bot should trade. Must end before 11th June 2020.
            customPrefix (str, optional): Sets a custom prefix for the generated log file. Defaults to None.
            customFolder (str, optional): Selects a folder within the logs folder to insert the log file into.
        
        Raises:
            DateException: Starting or end date selected don't respect maximum or minimum required

        Returns:
            dict: JSON file log in dict format, containing all iterations of the run
        """
        # Validate dates
        if startDate < Testing.minDate: 
            raise DateException("Starting date selected for test run is too small. Please select date after 1st Jan. 2011.")
        elif startDate + timedelta(days=period) > Testing.maxDate: 
            raise DateException("Period is too long. Please select a period ending before 11th June 2020.")
        
        testBot = Bot(Strategy(-1), startDate, -1)
        if customPrefix is not None: testBot.fileLoggerJSON.prefix = customPrefix
        if customFolder is not None: testBot.fileLoggerJSON.customFolder = customFolder
        testBot.initialise(funds, stockList, period)
        testBot.start()
        
        path: str = "logs/past/" + customFolder + "/" + testBot.fileLoggerJSON.getFileName()
        log: dict = Graphing.fetchLog(path)
        return log
    
    def populateStockObjs(stockList: list[str]) -> None:
        for stockName in stockList:
            Testing.StockObjs[stockName] = Stock(stockName)
    
    # Multiple test runs
    def testMultiple(
        iterations: int,
        strategies: list[TemplateDM] = [],
        funds:int = 1000,
        startDate: datetime = None,
        stockList: list[Stock] = None,
        periodLimits: tuple[int, int] = (10, 50),
        customFolder = None
        ) -> list:
        
        """Performs multiple tests with randomized values and returns a dict containing generated data.

        Args:
            iterations (int): Amount of test runs
            Strategies (list[DM]): Strategies which should be tested. Has to be filled with classes deriving from TemplateDM.
            funds (int, optional): Initial portfolio funds. Defaults to 1000.
            startDate (datetime, optional): Date at which trading should start. Defaults None, which uses a randomiser selecting random valid dates.
            stockList (list[Stock], optional): List of stocks to add to Portfolio. Defaults to None, which uses a randomiser selecting random top 20 NASDAQ stocks.
            periodLimits (tuple[int, int], optional): Sets the maximum and minimum limits for the trading period. For constant period pass single integer. Defaults to (20, 50).
            customFolder: name of the folder in which all logs / graphs should be saved
        
        Returns:
            list: Final portfolio values of all tests, list length is defined by the amount of strategies used
        """
        # Definitions based on parameters
        constantPeriod = True if type(periodLimits) is int else False
        
        results = []
        for strategy in strategies: results.append([])
        
        # pregenerate run-independent Stock objects for optimising price calls during validation
        if stockList is None:
            Testing.populateStockObjs(Testing.Nasdaq200B)
        else: Testing.populateStockObjs(stockList)
        
        # create subfolders for all associated logs and graphs associated
        # this is valid OS-safe pathlib syntax, very cool (https://stackoverflow.com/questions/61321503/is-there-a-pathlib-alternate-for-os-path-join)
        # also: https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
        if customFolder is None: customFolder = "Test_" + datetime.now().strftime(FileLoggerJSON.saveFormat)
        absPath = pathlib.Path().resolve()
        os.makedirs(absPath / "logs" / "past" / customFolder)
        os.makedirs(absPath / "output" / customFolder)
        for strategy in strategies: os.makedirs(absPath / "output" / customFolder / strategy.__name__)
        
        # test loop
        for i in range(iterations):
            print(f"Tests:\t Starting Test {i + 1}/{iterations}")
            # define period
            if not constantPeriod:
                runPeriod = random.randint(periodLimits[0], periodLimits[1])
            else: runPeriod = periodLimits
            
            # define date
            if startDate is None:
                # select random date between max and min
                maxDatePossible = Testing.maxDate - timedelta(days=runPeriod)
                dateDelta = maxDatePossible - Testing.minDate
                runDate = maxDatePossible- timedelta(days=random.randint(0, dateDelta.days))
            else: runDate = startDate
            
            # define portfolio
            if stockList is None:
                # Generate randomised stock list based on Nasdaq 200B+ companies list
                # As seen in: https://stackoverflow.com/questions/2612802/how-do-i-clone-a-list-so-that-it-doesnt-change-unexpectedly-after-assignment
                availableStocks = Testing.Nasdaq200B.copy()
                length = random.randint(2, len(availableStocks))
                
                runStocks = []
                for j in range(length):
                    # len() needs to be recalled as list length changes
                    # Since same stock can't be added twice
                    index = random.randint(0, len(availableStocks) - 1)
                    runStocks.append(availableStocks[index])
                    availableStocks.pop(index)
                        
            else: runStocks = stockList
            
            # removes nonexistent stocks from the stock list (E.g. if company didn't exist yet at timeline start)
            if Config.debug(): print(f"Tests:\t Checking Stock validities")
            for stockName in runStocks:
                if Config.debug(): print(f"Tests:\t Checking validity of {stockName}")
                
                consecutiveNoneCount = 0    
                testDate = datetime(runDate.year, runDate.month, runDate.day)
                
                # 4 dates in a row being exceptions is impossible if stock exists, stock must be invalid
                for j in range(4):
                    stockValue = Testing.StockObjs[stockName].getPrice(-1, testDate)
                    if stockValue is None: consecutiveNoneCount += 1

                    testDate = testDate - timedelta(days=1)
            
                if consecutiveNoneCount == 4: 
                    runStocks.remove(stockName)
                    if Config.debug(): print(f"Tests:\t {stockName} is invalid and has been removed")
                    
                elif Config.debug(): print(f"Tests:\t {stockName} is valid")
                
            # very rare but possible edgecase
            if len(runStocks) == 0:
                if Config.debug(): print(f"Tests:\t No valid stocks in portfolio. Skipping run.") 
                # has to be added else the runCount breaks in evaluation 
                for j in range(len(strategies)): results[j].append(funds)
                continue
            elif Config.debug(): print(f"Tests:\t Validity check finished, starting testing")
            
            # run tests, update values
            for j in range(len(strategies)):
                customPrefix = f"Run#{i+1}_{strategies[j].__name__}"
                log = Testing.testSingle(strategies[j], funds, runDate, runStocks, runPeriod, customPrefix, customFolder)
                value = Testing.getFinalValues(log)
                results[j].append(value)
        
        # Results contains lists with final portf values for each strat tested
        return results
            
    def getFinalValues(log: dict):
        """Utility function for getting the final portfolio value from a log file

        Args:
            log (dict): JSON log file in dict form

        Returns:
            float: Final value at end of run
        """
        # index -1 is last element in container
        totalValue = log["snapshots"][-1]["funds"]
        for stock in log["snapshots"][-1]["stocksHeld"]:
            stockValue = stock["value"] * stock["amount"]
            totalValue += stockValue
            
        return totalValue
    
    # Comparse two DMs, uses multiple tests
    def testTimeFrame(Strategy: TemplateDM, funds:int = 1000, startDate: datetime = "min", endDate: datetime = "max", ) -> None:
        """Testing function to test a Strategy during a specified timeframe. Used for debugging. Defaults to maximum time period.

        Args:
            Strategy (TemplateDM): Strategy to be tested
            funds (int, optional): Portfolio starting funds. Defaults to 1000.
            startDate (datetime, optional): Starting date of the run. Defaults to "min".
            endDate (datetime, optional): Date on which the run should end. Defaults to "max".

        """
        
        # Can't set Class properties as standard parameters for some reason, therefore using strings
        if startDate == "min": startDate = Testing.minDate
        if endDate == "max": endDate = Testing.maxDate
        
        period: timedelta = endDate - startDate
        period: int = period.days
        
        return Testing.testSingle(Strategy, funds, startDate, Testing.Nasdaq200B.copy(), period)
    
    def compareDMs(
        iterations: int,
        Strategies: [],
        funds:int = 1000,
        startDate: datetime = None,
        stockList: list[Stock] = None,
        periodLimits: tuple[int, int] = (10, 50)
        ) -> None:
        """Does multiple test runs using the settings given in the parameters.\n
        Evaluates these runs to find average profit, win count and create a histogram of all runs perfomed.

        Args:
            iterations (int): Amount of runs that should be done for each strategy
            Strategies (any valid DM): Strategies which should be compared
            funds (int, optional): Starting portfolio funds. Defaults to 1000.
            startDate (datetime, optional): Start date for each run. Leave at None for randomized start dates.
            stockList (list[Stock], optional): List of stocks used for each run. Leave at None for a randomized portfolio on each run.
            periodLimits (tuple[int, int], optional): Sets the trading period constraints. Defaults to (10, 50). Set to a single integer for constant period.
        """
        
        # The initial validation check tends to take a few seconds
        print("Tests:\t Starting Test run, this might take a few seconds")
        
        # Get start time for runtime display at the end of the testing process
        then = datetime.now()
        
        # Executes all comparison runs
        customFolder = "logs_" + datetime.now().strftime(FileLoggerJSON.saveFormat)
        data: tuple[list, list] = Testing.testMultiple(iterations, Strategies, funds, startDate, stockList, periodLimits, customFolder)
        
        # evaluate data generated from comparison runs
        runCount = len(data[0])
        stratCount = len(data)
    
        # Dynamically define start arrays
        wins, averageProfit, profits = [], [], []
        for j in range(stratCount):
            wins.append(0)
            averageProfit.append(0)
            profits.append([])
        
        # Populate arrays
        # For readablitiy, j always references strategies and i always refers to runs
        for i in range(runCount):
            # finalValues[j] = final value of jth strategy
            finalValues = []
            for j in range(stratCount):
                finalValues.append(data[j][i])
            
            # Determine average profits
            for j in range(stratCount): 
                profit = finalValues[j] - funds
                profits[j].append(profit)
                averageProfit[j] += profit
            
            # Determine winning strategy, add up wins
            winStratIndex = 0
            for j in range(stratCount - 1):
                if finalValues[j + 1] > finalValues[winStratIndex]:
                    winStratIndex = j + 1
            wins[winStratIndex] += 1
        
        for j in range(stratCount): averageProfit[j] = averageProfit[j] / runCount
        
        # format results
        result = "Test results:"
        
        # Determine overall winning strategy
        totalWinStratIndex = 0
        for i in range(len(wins) - 1):
            if wins[i + 1] > wins[totalWinStratIndex]:
                totalWinStratIndex = i + 1
        
        winStrategy = Strategies[totalWinStratIndex].__name__
        result += f"\nStrategy {winStrategy} was the superior Strategy."
        
        for j in range(len(Strategies)):
            result += f"\nStrategy {Strategies[j].__name__} has won in {str(wins[j])} / {str(runCount)} runs"
            result += f"\nAverage profit: {averageProfit[j]}"
        
        print(result)
        
        # save to output
        fileName = "TestResults" + "_" + datetime.now().strftime(FileLoggerJSON.saveFormat) + ".txt"
        filePath = f"output/{customFolder}/" + fileName
        with open(filePath, mode="a") as file: file.write(result)
        print(f"Tests:\t Saved result to {filePath}")
        
        # Create graph
        print("Tests:\t Creating comparison graph")
        Graphing.plotProfits(profits, Strategies, savePath=f"output/{customFolder}/")

        # Print runtime information
        now = datetime.now()
        runtime = now - then
        dateFormat = '%d. %m %Y %M:%H'
        print("Tests:\t Runtime information:")
        print(f"Start:\t {then.strftime(dateFormat)}\nEnd:\t {now.strftime(dateFormat)}\nTime:\t {runtime}")
        