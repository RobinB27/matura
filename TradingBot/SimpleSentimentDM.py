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
    
    def __init__(self, mode: int = 0):
        
        self.mode = mode
        self.previousScore = None
        
    def makeStockDecision(self, portfolio: Portfolio, ticker: str, mode: int, date: datetime) -> int:
        """makes a decision whether to buy a stock or not on a given date

        Args:
            portfolio (Portfolio): Portfolio to cultivate
            ticker (str): 
            mode (int, optional): Realtime or past mode. Defaults to 0. (past)
            dateStart (str, optional): Starting datestring for past mode. Defaults to "0".

        Returns:
            int: 1 = buy, None = hold, -1 = sell
        """
        
        # YYYY-MM-DD Format or refactor to using Datetime
        headlines = HistData.getHeadlinesDT(date, ticker)
        
        score = 0
        for headline in headlines:
            sentiment = getSentiment(headline["text"])
            score += SimpleSentimentDM.scoreTable[sentiment]
        
        if score > self.previousScore:
            self.previousScore = score
            return 1
        elif score < self.previousScore:
            self.previousScore = score
            return -1
        else: 
            self.previousScore = score
            return None