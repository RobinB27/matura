# This file contains the MACDDecisionMaking class. It decides if a given stock (see Stock.py) should be bought or sold on any given day or timestamp.
# To that effect it compares the values of the so called signal line against the macd line (see SignalLineCalculator.py) to determine if to buy or sell.
# On a more technical level it compares the two to determine if the signal line has corssed over the macd line. Depending on the type of crossing (from above or below) 
# it will give the decision to buy or sell a stock. If no crossing has occured it will return the decison to ignor the stock.
# The decisioon is then given to the bot itself (see Bot.py) to execute

from TradingBot.Portfolio import Portfolio
from TradingBot.FinancialCalculators.SignalLineCalculator import SignalLineCalculator

from Util.Config import Config


class MACDDecisionMaking:

    def __init__(self, mode: int = 0):

        self.mode = mode
        self.SignalLineCalculator = SignalLineCalculator()

        # curveComparison is from perspective of signal line
        # 1 -> signal line above MACD, 0 -> signal line = MACD, -1 -> signal line below MACD
        self.curveComparison = {}
        self.MACDValuesDict = {}
        self.SignalLineValuesDict = {}

        self.iterations = 0

    def getPreviousDate(self, portfolio: Portfolio, dateToCalculate: str) -> str:
        # NOTE: Refactor things like subtractDayFromDate into class functions instead of object functions, also rework using dateTimes
        # checks for weekend and exceptions
        previousDate = portfolio.subtractDayFromDate(dateToCalculate)

        # checks for crossovers
        while previousDate not in self.curveComparison:
            previousDate = portfolio.subtractDayFromDate(previousDate)

        return previousDate

    def update(self, portfolio: Portfolio, ticker: str, mode: int, dateToCalculate: str, interval: int= 0) -> None:
        """Utility function to update all value dicts. Only intended for use in class MACDDecisionMaking

        Args:
            dateToCalculate (str): date in use for the current iteration
            placeholderResult (tuple): place holder result gained from SignalLineCalculator class
        Returns:
            None, updates the object's curveComparison dict
        """

        # Get placeholder date
        if mode == 0:
            placeholderResult = self.SignalLineCalculator.signalLineCalculation(portfolio, ticker, mode, dateToCalculate, interval)
        elif mode  == -1:
            placeholderResult = self.SignalLineCalculator.signalLineCalculation(portfolio, ticker, mode, dateToCalculate)

        # Update MACD & Signal line
        self.MACDValuesDict[dateToCalculate] = placeholderResult[0]
        self.SignalLineValuesDict[dateToCalculate] = placeholderResult[1]

        # Update curveComparison
        if self.SignalLineValuesDict[dateToCalculate] > self.MACDValuesDict[dateToCalculate]:
            if Config.debug():
                print(f"MACDDecisionMaking: MACDPlaceholder: {self.MACDValuesDict[dateToCalculate]} > signalLine: {self.SignalLineValuesDict[dateToCalculate]}")
            self.curveComparison[dateToCalculate] = 1

        elif self.SignalLineValuesDict[dateToCalculate] < self.MACDValuesDict[dateToCalculate]:
            if Config.debug():
                print(f"MACDDecisionMaking: MACDPlaceholder: {self.MACDValuesDict[dateToCalculate]} < signalLine: {self.SignalLineValuesDict[dateToCalculate]}")
            self.curveComparison[dateToCalculate] = -1

        else:
            self.curveComparison[dateToCalculate] = 0

    def makeStockDecision(self, portfolio: Portfolio, ticker: str, mode: int = 0, dateToCalculate: str = "0"):
        """Makes a decision on whether to buy a stock or not on a given date.

        Args:
            portfolio (Portfolio): Portfolio to be modified
            ticker (str): Stock ticker for which a decision should be made
            mode (int, optional): Mode of the bot. Defaults to 0. (past mode)
            dateToCalculate (str, optional): Date for which the decision should be made. Defaults to "0". NOTE: Change this to use datetimes and make it non-optional

        Returns:
            decision in a binary format where 0 is no and 1 is yes, other response means stock is held
        """
        # Value update happens regardless of iteration
        self.update(portfolio, ticker, mode, dateToCalculate)
        self.iterations += 1;

        if self.iterations == 2:
            # Special actions for second iteration only

            # checks for weekend and exceptions
            previousDate = self.getPreviousDate(portfolio, dateToCalculate)

            # Final decision making, reduced for 2nd iteration
            if self.curveComparison[previousDate] == -1 and self.curveComparison[dateToCalculate] == 1:
                if Config.debug():
                    print(
                        f"MACDDecisionMaking:\t Bullish Crossover on {dateToCalculate}")
                return 1
            elif self.curveComparison[previousDate] == 1 and self.curveComparison[dateToCalculate] == -1:
                if Config.debug():
                    print(
                        f"MACDDecisionMaking:\t Bearish Crossover on {dateToCalculate}")
                return -1
            else:
                return None

        elif self.iterations < 2:
            # Special actions for 3rd iteration and upwards

            # checks for weekend, exceptions & crossover
            previousDate = self.getPreviousDate(portfolio, dateToCalculate)

            # NOTE: Doesn't this calculate the same thing as previousDate?
            DayBeforePreviousDate = portfolio.subtractDayFromDate(dateToCalculate)

            while DayBeforePreviousDate not in self.curveComparison:
                DayBeforePreviousDate = portfolio.subtractDayFromDate(DayBeforePreviousDate)

            # Final general decision making
            if self.curveComparison[previousDate] == -1 and self.curveComparison[dateToCalculate] == 1:
                if Config.debug():
                    print(
                        f"MACDDecisionMaking:\t Bullish Crossover on {dateToCalculate}")
                return 1
            elif self.curveComparison[DayBeforePreviousDate] == -1 and self.curveComparison[previousDate] == 0 and self.curveComparison[dateToCalculate] == 1:
                if Config.debug():
                    print(
                        f"MACDDecisionMaking:\t Bullish Crossover on {dateToCalculate}")
                return 1
            elif self.curveComparison[previousDate] == 1 and self.curveComparison[dateToCalculate] == -1:
                if Config.debug():
                    print(
                        f"MACDDecisionMaking:\t Bearish Crossover on {dateToCalculate}")
                return -1
            elif self.curveComparison[DayBeforePreviousDate] == 1 and self.curveComparison[previousDate] == 0 and self.curveComparison[dateToCalculate] == -1:
                if Config.debug():
                    print(
                        f"MACDDecisionMaking:\t Bearish Crossover on {dateToCalculate}")
                return -1
            else:
                return None
