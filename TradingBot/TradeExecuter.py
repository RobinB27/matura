from TradingBot.MACDDecisionMaking import MACDDecisionMaking
from TradingBot.Portfolio import Portfolio

def TradeExecuter(self):
    
    #classMethod will encompass the whole act of making a trade for a stock -> decision making and executing decision
    #such that the bot can map the function onto all iterables in portfolio.stocksHeld
    @classmethod
    def executeTrade(self, portfolio):
        pass