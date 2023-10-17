# Copyright (C) 2022 Robin Bacher and Lucien Gees
# This file is part of the "Automated Stock Trading Using News Headlines" matura project.
# Last edited on 17/10/2023

# This file implements the AverageSentimentDM (DecisionMaking)
# This DecisionMaking class implements a trading strategy based on Sentiment Analysis.
# The Strategy is the main Sentiment Analysis based trading strategy that this project is testing.

from datetime import datetime, timedelta

from TradingBot.Portfolio import Portfolio
from Util.Config import Config
from Util.DateHelper import DateHelper
from HistoricalData.HistData import HistData
from SentimentAnalysis.Classification import getSentiment
from WebScraping.YahooFinance.Webscraper import YahooWebScraper as WebScraper

class AvgSentimentDM:
    """
    Simple sentiment analysis based Decision making\n
    This Class acts as the template class for all other sentiment analysis based Decision Making classes.\n
    The Algorithm implemented here is very simple and intended to be a technical testing device for\n
    all systems required for sentiment analysis instead of actual trading data generation.
    """
    
    abbreviation = "ASDM"
    
    scoreTable = {
        'positive': 1,
        'neutral': 0,
        'negative': -1
    }
    
    def __init__(self, mode: int):
        self.mode = mode
        # Bot mode
        self.weighted = Config.getParam("SentimentScoreWeighted")
        # Uses weighted sentiment scores: score * headlinecount 
        self.stockMax = Config.getParam("SentimentMaxStocks")
        # Specifies the maximum amount of a stock the Strategy can buy until it stopts to send buy signals
        self.pastSentimentScores = {}
        self.pastEMA = {}
        self.pastMACD = {}
        self.pastMACDEMA = {}
        # Access all with ["date"] => value, use DateHelper
        self.stocksOwned = 0
    
    def getSMA(self, date: datetime, period: int, ticker:str, MACD = False) -> int:
        """ Calculate the SMA value using Sentiment scores.

        Args:
            date (datetime): Starting date
            period (int): Amount of days to use

        Returns:
            int: SMA value
        """
        # formula from https://www.investopedia.com/terms/m/movingaverage.asp
        scoreSum = 0
        for day in range(period):
            if MACD: scoreSum += self.getMACD(date, ticker)
            else: scoreSum += self.getScore(date, ticker)
            date -= timedelta(days=1)
            
        return scoreSum / period
    
    
    def getEMA(self, date: datetime, period: int, ticker:str, MACD = False, pastEMACalc = False) -> int:
        """ Calculate the EMA value using Sentiment scores

        Args:
            date (datetime): Starting date
            period (int): Amount of days to use

        Returns:
            int: EMA Value
        """
        # formula from https://www.investopedia.com/terms/m/movingaverage.asp
        dateStr = DateHelper.format(date)
        # Check cache, checks sadly can't be added into one line since that could crash
        if MACD and dateStr in self.pastMACDEMA:
            if str(period) in self.pastMACDEMA[dateStr]:
                return self.pastMACDEMA[dateStr][str(period)]
        elif dateStr in self.pastEMA: 
            if str(period) in self.pastEMA[dateStr]:
                return self.pastEMA[dateStr][str(period)]
        
        SMA = self.getSMA(date, period, ticker, MACD)
        
        # Smoothing defines how heavily recent events should be weighed, 2 is used here since it's the most common value used for smoothing
        smoothing = 2
        multiplier = (smoothing / (1 + period))
        
        # get previous EMA
        prevDateStr = DateHelper.format(date - timedelta(days=1))
        pastEMA = 0
        
        if pastEMACalc: pastEMA = 0
        elif MACD and prevDateStr in self.pastMACDEMA: 
            if str(period) in self.pastMACDEMA[prevDateStr]:
                pastEMA = self.pastMACDEMA[prevDateStr][str(period)]
        elif MACD and prevDateStr not in self.pastMACDEMA: pastEMA = self.getEMA(date - timedelta(1), period, ticker, True, True)
        elif prevDateStr in self.pastEMA: 
            if str(period) in self.pastEMA:
                pastEMA = self.pastEMA[prevDateStr][str(period)]
        else: pastEMA = self.getEMA(date - timedelta(1), period, ticker, False, True)
        
        EMA = SMA * multiplier + pastEMA * multiplier
        
        # Add to cache
        if not MACD and dateStr in self.pastEMA: 
            self.pastEMA[dateStr][str(period)] = EMA
        elif not MACD and dateStr not in self.pastEMA:
            self.pastEMA[dateStr] = {str(period): EMA}
        elif MACD and dateStr in self.pastMACDEMA:
            self.pastMACDEMA[dateStr][str(period)] = EMA
        elif MACD and dateStr not in self.pastMACDEMA:
            self.pastMACDEMA[dateStr] = {str(period): EMA}
            
        # Alternative version, same function
        """         
        if not MACD:
            if dateStr in self.pasEMA:
                self.pastEMA[dateStr][str(period)] = EMA
            else:
                self.pastEMA[dateStr] = {str(period): EMA}
        elif dateStr in self.pastMACDEMA:
            self.pastMACDEMA[dateStr][str(period)] = EMA
        else:
            self.pastMACDEMA[dateStr] = {str(period): EMA} 
        """
        
        return EMA
    
    def getMACD(self, date: datetime, ticker:str) -> int:
        """Calculate the MACD value using Sentiment scores

        Args:
            date (datetime): Date to calculate

        Returns:
            int: MACD value
        """
        if DateHelper.format(date) in self.pastMACD: return self.pastMACD[DateHelper.format(date)]
        MACD = self.getEMA(date, 12, ticker) - self.getEMA(date, 26, ticker)
        self.pastMACD[DateHelper.format(date)] = MACD
        return MACD
    
    def getSIG(self, date: datetime, ticker) -> int: 
        """Calculate the Signal line value using Sentiment scores

        Args:
            date (datetime): Date to calculate

        Returns:
            int: Signal line value
        """
        return self.getEMA(date, 9, ticker, True)
    
    def checkCrossover(self, date, ticker) -> int: 
        """Check whether the MACD crosses over the Signal line

        Args:
            date (datetime): date to evaluate

        Returns:
            int: 0 = no crossover, 1 = crossover from below (buy), -1 = crossover from above (sell)
        """
        prevDate = date - timedelta(days=1)
        if self.getSIG(prevDate, ticker) < self.getMACD(prevDate, ticker): previouslyBelow = True
        else: previouslyBelow = False
        
        if self.getSIG(date, ticker) < self.getMACD(date, ticker): nowBelow = True
        else: nowBelow = False
        
        # If a change happened, a crossover happened
        crossoverHappened = previouslyBelow != nowBelow
        # evaluate type of crossover
        if crossoverHappened and previouslyBelow: 
            # buy order
            if Config.debug(): print(f"DM:\t Positive crossover detected.")
            if self.stocksOwned < self.stockMax:
                self.stocksOwned += 1
                return 1
            else: 
                if Config.debug(): print(f"DM:\t Couldn't buy {ticker} because Stock maximum {self.stockMax} was reached.")
                return 0
        elif crossoverHappened and not previouslyBelow: 
            # sell order
            if Config.debug(): print(f"DM:\t Negative crossover detected.")
            if self.stocksOwned > 0: self.stocksOwned -= 1
            return -1
        else: 
            # ignore order
            if Config.debug(): print(f"DM:\t No crossover detected.")
            return 0
    
    def getScore(self, date: datetime, ticker: str) -> int:
        """Calculates the sentiment score for any given date

        Args:
            day (datetime): date to calculate

        Raises:
            Exception: Exception raised if mode parameter is invalid
        """
        
        if DateHelper.format(date) not in self.pastSentimentScores:
            # mode-dependant headline retrieval
            if self.mode == -1: headlines = HistData.getHeadlinesDT(date, ticker)
            elif self.mode == 0: headlines = WebScraper.getHeadlines(ticker)
            else: raise Exception("Invalid mode selection for AvgSentimentDM")
            
            score = 0
            
            # Process headlines, if headlines exist
            if headlines is not None:
                count = len(headlines)
                if Config.debug(): print(f"DM:\t Found {count} relevant headlines for {ticker} on {DateHelper.format(date)}")
                
                # calculate sentiment score
                for headline in headlines:
                    if self.mode == 0:
                        sentiment = getSentiment(headline.text)
                    else:
                        sentiment = getSentiment(headline["text"])
                    score += AvgSentimentDM.scoreTable[sentiment]
                if self.weighted: score = score * count
                
            elif Config.debug(): print(f"DM:\t Found no relevant headlines")
            
            # Debug logging
            if Config.debug():
                if self.weighted: print(f"DM\t Weighted sentiment score: {score}")
                else: print(f"DM\t Sentiment score: {score}")
            
            self.pastSentimentScores[DateHelper.format(date)] = score
            return score
        
        else: return self.pastSentimentScores[DateHelper.format(date)]
        
    def makeStockDecision(self, portfolio: Portfolio, ticker: str, mode: int, date: datetime, interval: int = None) -> int:
        # NOTE: Make Ticker an object var for all DMs since it is a constant anyway
        """makes a decision whether to buy a stock or not on a given date

        Args:
            portfolio (Portfolio): Portfolio
            ticker (str): Stock ticker for which decision should be made
            mode (int): Realtime (0) or historical data (-1) mode.
            date (datetime): Date for when the decision should be made
            interval (int, optional): interval at which trading happens in realtime mode. Default to None, not required for historical data mode

        Returns:
            int: 1 = buy, None = hold, -1 = sell
        """
        
        return self.checkCrossover(date, ticker)