# This file implements the FileLoggerJSON class.
# The FileLoggerJSON class generates a JSON file representation of a portfolio
# that the bot has created. The files produced by this logger are used by the
# class Graphing to produce the visualisations which are shown at the end of every bot run.

import json, os
from datetime import datetime

from TradingBot.Portfolio import Portfolio
from Util.DateHelper import DateHelper

# Add error handling for file handling, best practice
# Add parser

class FileLoggerJSON:
    """
    Utility class to log all contents of a portfolio class to a JSON file. \n
    Subsequent snapshots of a run are saved within the same file provided the same File Logger is used
    """
    # NOTE: If two logs are created during the same millisecond, the logger will break and append to the previous file. This is ignored as the chance of this happening is impossibly low
    saveFormat = "%d_%b_%y_%I_%M_%f_%p"
    timeStampFormat = "%d-%m-%y-%H-%M" # can be in minutes as intervals are always at least one minute
    
    def __init__(self, prefix:str = "run" ,path: str = "logs") -> None:
        self.dirPath = path
        self.fileName = prefix + "_" + datetime.now().strftime(FileLoggerJSON.saveFormat) + ".json"
    
    def snapshot(self, portfolio: Portfolio, mode: int, date: datetime, interval: int = None, strategy = None) -> None:
        """Updates the JSON file log associated with this instance of the FileLoggerJSON class.

        Args:
            portfolio (Portfolio): Portfolio to log
            mode (int): Current bot mode (0 or -1)
            date (str): The current date or timestamp of the iteration, format depends on mode
            interval (int, optional): Interval at which the bot is trading, only needed in realtime mode. Defaults to None.
        """
        filePath = os.path.join(self.dirPath, self.fileName)
        
        # Retrieve file content
        content = ""
        
        # If file doesn't exist yet, add empty JSON template
        try: 
            with open(filePath, 'r') as log: content = log.read().replace('\n', '')
        except FileNotFoundError:
            content = '{"snapshots": []}'
            content = json.loads(content)
            content["strategyName"] = strategy.__name__
            content = json.dumps(content)
            
        # Update file content based on data in Portfolio
        content = json.loads(content);
        
        pObject = {
            "funds": portfolio.funds,
            "stocksHeld": []
        }
        
        # Date has different meaning depending on mode
        if mode == -1:
            pObject["date"] = DateHelper.format(date)
        elif mode == 0:
            pObject["timeStamp"] = date.strftime(FileLoggerJSON.timeStampFormat)
            pObject["interval"] = interval # NOTE: could be saved in content instead of snapshot as the interval is constant
        
        for stock in portfolio.getStocks():
            sObject = {
                    "name": stock.ticker,
                    "amount": stock.amount,
                    "value": "undefined"
                }
            
            if mode == 0:
                value = stock.amount * stock.getPrice() 
            elif mode == -1:
                #check to ensure no None prices cause an error
                stockValue = stock.getPrice(-1, date)
                if stockValue is None: stockValue = 0
                value = stock.amount * stockValue
                
            sObject["value"] = value
            pObject["stocksHeld"].append(sObject)
        
        content["snapshots"].append(pObject)
        
        content = json.dumps(content)
        
        # Write content to file
        with open(filePath, "w") as log: log.write(content)