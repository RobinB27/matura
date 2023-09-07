# This file implements the SimpleSentimentDM (DecisionMaking)
# This DecisionMaking class implements a trading strategy based on Sentiment Analysis.
# The Strategy is very simple and primarily used as a testing device to see whether the
# different features required for any Sentiment Analysis based strategy work without error.
# (Specifically the Sentiment Classifier itself, the Historical Dataset and the Web Scraper)

from datetime import datetime

from TradingBot.Portfolio import Portfolio
from Util.Config import Config
from HistoricalData.HistData import HistData
from SentimentAnalysis.Classification import getSentiment
from WebScraping.YahooFinance.Webscraper import YahooWebScraper as WebScraper

class SimpleSentimentDM:
    """
    Simple sentiment analysis based Decision making\n
    This Class acts as the template class for all other sentiment analysis based Decision Making classes.\n
    The Algorithm implemented here is very simple and intended to be a technical testing device for\n
    all systems required for sentiment analysis instead of actual trading data generation.
    """
    
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
        self.threshold = Config.getParam("SentimentScoreThreshold")
        # Specifies a theshold difference in sentiment score required to sell / buy
        self.previousScore = None
        # Previous score for comparison 
        
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
        
        # mode-dependant headline retrieval
        if mode == -1: headlines = HistData.getHeadlinesDT(date, ticker)
        elif mode == 0: headlines = WebScraper.getHeadlines(ticker)
        else: raise Exception("Invalid mode selection for SimpleSentimentDM")
        
        score = 0
        
        # Process headlines, if headlines are there
        if headlines is not None:
            count = len(headlines)
            if Config.debug(): print(f"DM:\t Found {count} relevant headlines")
            
            # calculate sentiment score
            for headline in headlines:
                sentiment = getSentiment(headline["text"])
                score += SimpleSentimentDM.scoreTable[sentiment]
            if self.weighted: score = score * count
            
        elif Config.debug(): print(f"DM:\t Found no relevant headlines")
        
        # Debug logging
        if Config.debug():
            if self.weighted: print(f"DM\t Weighted sentiment score: {score}")
            else: print(f"DM\t Sentiment score: {score}")
        
        if self.previousScore is None: self.previousScore = score
        
        # Pos = buy, Neg = sell
        scoreDifference = score - self.previousScore
        if abs(scoreDifference) >= self.threshold:
            if Config.debug(): print(f"DM:\t Threshold {self.threshold} passed.")
            
            if scoreDifference > 0:
                self.previousScore = score
                return 1

            elif scoreDifference < 0:
                self.previousScore = score
                return -1
            else: 
                self.previousScore = score
                return None
        else:
            if Config.debug(): print(f"DM:\t Threshold {self.threshold} not passed.")
            return None