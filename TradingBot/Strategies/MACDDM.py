# This file contains the MACDDecisionMaking class. It decides if a given stock (see Stock.py) should be bought or sold on any given day or timestamp.
# To that effect it compares the values of the so called signal line against the macd line (see SignalLineCalculator.py) to determine if to buy or sell.
# On a more technical level it compares the two to determine if the signal line has corssed over the macd line. Depending on the type of crossing (from above or below) 
# it will give the decision to buy or sell a stock. If no crossing has occured it will return the decison to ignor the stock.
# The decision is then given to the bot itself (see Bot.py) to execute

from datetime import datetime, timedelta

from TradingBot.Portfolio import Portfolio
from TradingBot.SignalLineCalculator import SignalLineCalculator

from Util.Config import Config
from Util.DateHelper import DateHelper


class MACDDM:
    """Class that implements a trading strategy based on the MACD indicator. Can be passed to the bot to be used as a trading strategy."""

    def __init__(self, mode: int = 0):

        self.mode = mode
        self.SignalLineCalculator = SignalLineCalculator()

        # curveComparison is from perspective of signal line
        # 1 -> signal line above MACD, 0 -> signal line = MACD, -1 -> signal line below MACD
        self.curveComparison = {}
        self.MACDValuesDict = {}
        self.SignalLineValuesDict = {}
        
        self.currentTimes = []
        self.timeInstancesElapsed = -1 # starts at -1 so first call of update method doesnt destroy accesses to the dict self.currentTimes

        self.iterations = 0

    def getPreviousDate(self, date: datetime) -> datetime:
        # checks for weekend and exceptions
        previousDate = date - timedelta(days=1)

        # checks for crossovers
        while DateHelper.format(previousDate) not in self.curveComparison:
            previousDate = previousDate - timedelta(days=1)

        return previousDate

    def update(self, portfolio: Portfolio, ticker: str, mode: int, date: datetime = None, interval: int = None) -> None:
        """Utility function to update all value dicts. Only intended for use in class MACDDecisionMaking

        Args:
            dateToCalculate (str): date in use for the current iteration
            placeholderResult (tuple): place holder result gained from SignalLineCalculator class
        Returns:
            None, updates the object's curveComparison dict
        """

        placeholderResult = self.SignalLineCalculator.signalLineCalculation(portfolio, ticker, mode, date, interval)

        # define key based on mode
        if mode == 0 and interval is not None:
            # realtime mode
            timeForKey = datetime.now()
            timeForKey = timeForKey.strftime("%Y-%m-%d-%H-%M")
            key = ticker + "_" + timeForKey
            
            self.currentTimes.append(key)
            
            self.timeInstancesElapsed += 1
        elif mode == -1:
            # historical data
            key = DateHelper.format(date)

        # Update MACD & Signal line
        self.MACDValuesDict[key] = placeholderResult[0]
        self.SignalLineValuesDict[key] = placeholderResult[1]

        # Update curveComparison
        if self.SignalLineValuesDict[key] > self.MACDValuesDict[key]:
            if Config.debug():
                print(f"MACD:\t MACDPlaceholder: {self.MACDValuesDict[key]} > signalLine: {self.SignalLineValuesDict[key]}")
            self.curveComparison[key] = 1

        elif self.SignalLineValuesDict[key] < self.MACDValuesDict[key]:
            if Config.debug():
                print(f"MACD:\t MACDPlaceholder: {self.MACDValuesDict[key]} < signalLine: {self.SignalLineValuesDict[key]}")
            self.curveComparison[key] = -1

        else:
            self.curveComparison[key] = 0

    def makeStockDecision(self, portfolio: Portfolio, ticker: str, mode: int = 0, date: datetime = None, interval: int = 0) -> int:
        """Makes a decision on whether to buy a stock or not on a given date.

        Args:
            portfolio (Portfolio): Portfolio to be modified
            ticker (str): Stock ticker for which a decision should be made
            mode (int): Mode of the bot.
            date (str, optional): Date for the decision, required in historical data mode.

        Returns:
            decision in a binary format where 0 is no and 1 is yes, other response means stock is held
        """
        # Value update happens regardless of iteration
        
        self.update(portfolio, ticker, mode, date, interval)
        self.iterations += 1

        if self.iterations == 2:
            # Special actions for second iteration only

            if mode == -1:
                # Historical data
                value = date
                prevValue = self.getPreviousDate(value)
                value = DateHelper.format(value)
                prevValue = DateHelper.format(prevValue)
            elif mode == 0:
                # realtime mode
                value = self.currentTimes[self.timeInstancesElapsed]
                prevValue = self.currentTimes[self.timeInstancesElapsed -1]

            # Final decision making, reduced for 2nd iteration
            if self.curveComparison[prevValue] == -1 and self.curveComparison[value] == 1:
                if Config.debug():
                    print(
                        f"MACD:\t Bullish Crossover on {value}")
                return 1
            elif self.curveComparison[prevValue] == 1 and self.curveComparison[value] == -1:
                if Config.debug():
                    print(
                        f"MACD:\t Bearish Crossover on {value}")
                return -1
            else:
                return None

        elif self.iterations > 2:
            # Special actions for 3rd iteration and upwards

            if mode == -1:
                # Historical data
                value = date
                prevValue = self.getPreviousDate(value)
                valueBeforePreviousValue = self.getPreviousDate(prevValue)
            elif mode == 0:
                # realtime mode
                value = self.currentTimes[self.timeInstancesElapsed]
                prevValue = self.currentTimes[self.timeInstancesElapsed -1]
                valueBeforePreviousValue = self.currentTimes[self.timeInstancesElapsed -2]
            
            if mode == -1: # only needed in past mode
                while DateHelper.format(valueBeforePreviousValue) not in self.curveComparison:
                    valueBeforePreviousValue = valueBeforePreviousValue - timedelta(days=1)
                
            value = DateHelper.format(value)
            prevValue = DateHelper.format(prevValue)
            valueBeforePreviousValue = DateHelper.format(valueBeforePreviousValue)

            # Final general decision making
            if self.curveComparison[prevValue] == -1 and self.curveComparison[value] == 1:
                if Config.debug():
                    print(
                        f"MACD:\t Bullish Crossover on {value}")
                return 1
            elif self.curveComparison[valueBeforePreviousValue] == -1 and self.curveComparison[prevValue] == 0 and self.curveComparison[value] == 1:
                if Config.debug():
                    print(
                        f"MACD:\t Bullish Crossover on {value}")
                return 1
            elif self.curveComparison[prevValue] == 1 and self.curveComparison[value] == -1:
                if Config.debug():
                    print(
                        f"MACD:\t Bearish Crossover on {value}")
                return -1
            elif self.curveComparison[valueBeforePreviousValue] == 1 and self.curveComparison[prevValue] == 0 and self.curveComparison[value] == -1:
                if Config.debug():
                    print(
                        f"MACD:\t Bearish Crossover on {value}")
                return -1
            else:
                return None        
