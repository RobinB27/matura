# This class implements several methods used for evaluating the viability of a trading strategy and for comparing strategies
from datetime import datetime, timedelta
import random

from TradingBot.Bot import Bot
from TradingBot.Stock import Stock
from TradingBot.TemplateDM import TemplateDM
from TradingBot.FileLoggers.FileLoggerJSON import FileLoggerJSON

from Util.Graphing import Graphing
from Util.Config import Config

# As described in https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
class DateException(Exception): pass

class Testing:
    
    maxDate = datetime(2020, 6, 11)
    # Technically goes back to 14 Feb 2009, but data amount stabilises at 2011
    minDate = datetime(2011, 1, 1)
    dateDelta = maxDate - minDate
    
    # As seen on 10/09/2023
    # from: https://www.nasdaq.com/market-activity/stocks/screener
    Nasdaq200B = ["AAPL", "MSFT", "GOOG", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "AVGO", "ADBE", "ASML", "COST", "PEP", "CSCO"]
    
    # single run
    def testSingle(Strategy: TemplateDM, funds: int, startDate: datetime, stockList: list[Stock], period: int) -> dict:
        """Does a single test run with the specified parameters and returns the path to the produced log

        Args:
            Strategy (TemplateDM): Valid DecisionMaking class which should be used
            startDate (datetime): Date at which trading should start. Must be after 1st January 2011.
            funds (int): Initial portfolio funds
            stockList (list[Stock]): List of stocks to add to Portfolio
            period (int): Amount of days for which bot should trade. Must end before 11th June 2020.
        
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
        testBot.initialise(funds, stockList, period)
        testBot.start()
        
        path: str = "logs/" + testBot.fileLoggerJSON.fileName
        log: dict = Graphing.fetchLog(path)
        return log
    
    # Multiple test runs
    def testMultiple(
        iterations: int,
        Strategy: TemplateDM,
        Strategy2: TemplateDM = None,
        funds:int = 1000,
        startDate: datetime = None,
        stockList: list[Stock] = None,
        periodLimits: tuple[int, int] = (10, 50)
        ) -> list:
        
        """Performs multiple tests with randomized values and returns a dict containing generated data.

        Args:
            iterations (int): Amount of test runs
            Strategy (TemplateDM): Valid DecisionMaking class which should be used
            Strategy2 (TemplateDM): Second DecisionMaking class which should be used on identical data. Defaults to None.
            funds (int, optional): Initial portfolio funds. Defaults to 1000.
            startDate (datetime, optional): Date at which trading should start. Defaults None, which uses a randomiser selecting random valid dates.
            stockList (list[Stock], optional): List of stocks to add to Portfolio. Defaults to None, which uses a randomiser selecting random top 20 NASDAQ stocks.
            periodLimits (tuple[int, int], optional): Sets the maximum and minimum limits for the trading period. For constant period pass single integer. Defaults to (20, 50).
        
        Returns:
            list: Final portfolio valus of all tests, list contains two seperate lists if two strategies were used
        """
        # Definitions based on parameters
        constantPeriod = True if type(periodLimits) is int else False
        results = [] if Strategy2 is None else [[], []]
        
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
                runDate = Testing.maxDate - timedelta(days=random.randint(0, Testing.dateDelta.days))
            else: runDate = startDate
            
            # define portfolio
            if stockList is None:
                # As seen in: https://stackoverflow.com/questions/2612802/how-do-i-clone-a-list-so-that-it-doesnt-change-unexpectedly-after-assignment
                availableStocks = Testing.Nasdaq200B.copy()
                length = random.randint(2, len(availableStocks))
                runStocks = []
                for i in range(length):
                    # len() needs to be recalled as list length changes
                    # Since same stock can't be added twice
                    index = random.randint(0, len(availableStocks) - 1)
                    runStocks.append(availableStocks[index])
                    availableStocks.pop(index)
            else: runStocks = stockList
            
            # run tests, gather final value
            log = Testing.testSingle(Strategy, funds, runDate, runStocks, runPeriod)
            value = Testing.sumValue(log)
            if Strategy2 is not None:
                # Do second run, assume results has 2 lists
                log2 = Testing.testSingle(Strategy2, funds, runDate, runStocks, runPeriod)
                value2 = Testing.sumValue(log2)
                
                results[0].append(value)
                results[1].append(value2)
            else:
                results.append(value)
        
        return results
            
    def sumValue(log: dict):
        """Utility function for getting the final portfolio value from a log file

        Args:
            log (dict): JSON log file in dict form

        Returns:
            float: Final value at end of run
        """
        lastIndex = len(log["snapshots"]) - 1
        
        value = log["snapshots"][lastIndex]["funds"]
        for stock in log["snapshots"][lastIndex]["stocksHeld"]:
            value += stock["value"] * stock["amount"]
            
        return value
    
    # Comparse two DMs, uses multiple tests
    def compareDMs(
        iterations: int,
        Strategy: TemplateDM,
        Strategy2: TemplateDM,
        funds:int = 1000,
        startDate: datetime = None,
        stockList: list[Stock] = None,
        periodLimits: tuple[int, int] = (10, 50)
        ) -> None:
        
        
        
        data: tuple[list, list] = Testing.testMultiple(iterations, Strategy, Strategy2, funds, startDate, stockList, periodLimits)
        
        # evaluate data generated from comparison runs
        wins = [0 , 0]
        averageProfit = [0, 0]
        
        runs = len(data[0])
        for i in range(runs):
            values = [data[0][i], data[1][i]]
            
            for i in range(2): averageProfit[i] += (values[i] - funds)
            
            if values[0] > values[1]: wins[0] += 1
            else: wins[1] += 1
        
        for i in range(2): averageProfit[i] = averageProfit[i] / runs
        
        # format results
        result = ""
        if wins[0] > wins[1]:
            result += f"Strategy {type(Strategy).__name__} has outperformed Strategy {type(Strategy2).__name__}.\n"
            result += f"Strategy {type(Strategy).__name__} won in {wins[0] - wins[1]} runs out of {wins[0] + wins[1]}.\n"
        else:
            result += f"Strategy {type(Strategy2).__name__} has outperformed Strategy {type(Strategy).__name__}.\n"
            result += f"Strategy {type(Strategy2).__name__} won in {wins[1] - wins[0]} runs out of {wins[0] + wins[1]}.\n"
        
        result += "\n"
        
        result += f"Strategy {type(Strategy).__name__} average profit:\t {averageProfit[0]}\n"
        result += f"Strategy {type(Strategy2).__name__} average profit:\t {averageProfit[1]}\n"
        
        # save to output
        fileName = "TestResults" + "_" + datetime.now().strftime(FileLoggerJSON.saveFormat) + ".txt"
        filePath = "output/" + fileName
        
        print(result)
        with open(filePath, mode="a") as file: file.write(result)
        print(f"Tests:\n Saved result to {filePath}")
        