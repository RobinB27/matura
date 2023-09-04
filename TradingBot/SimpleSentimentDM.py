# This file implements the SimpleSentimentDM (DecisionMaking)
# This DecisionMaking class implements a trading strategy based on Sentiment Analysis.
# The Strategy is very simple and primarily used as a testing device to see whether the
# different features required for any Sentiment Analysis based strategy work without error.
# (Specifically the Sentiment Classifier itself and the Historical Dataset)

from datetime import datetime

from TradingBot.Portfolio import Portfolio
from Util.Config import Config
from HistoricalData.HistData import HistData
from SentimentAnalysis.Classification import getSentiment

class SimpleSentimentDM:
    """
    Sentiment Analysis based Decision making
    
    Needs to be reinstated for every seperate Stock.
    """
    
    scoreTable = {
        'positive': 1,
        'neutral': 0,
        'negative': -1
    }
    
    def __init__(self, mode: int):
        
        self.mode = mode
        self.previousScore = None
        
    def makeStockDecision(self, portfolio: Portfolio, ticker: str, mode: int, date: datetime, interval: int = None) -> int:
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
        
        if mode == 0: raise Exception("Not implemented")
        
        # YYYY-MM-DD Format or refactor to using Datetime
        headlines = HistData.getHeadlinesDT(date, ticker)
        
        score = 0
        
        # Process headlines, if headlines are there
        if headlines is not None:
            for headline in headlines:
                sentiment = getSentiment(headline["text"])
                score += SimpleSentimentDM.scoreTable[sentiment]
        
        if self.previousScore is None: self.previousScore = score
        
        if score > self.previousScore:
            self.previousScore = score
            return 1

        elif score < self.previousScore:
            self.previousScore = score
            return -1
        else: 
            self.previousScore = score
            return None