# This file implements the FileLoggerTXT class.
# The FileLoggerTXT class generates a FileLoggerTXT file representation of a portfolio
# that the bot has created. The files produced by this logger are used to gain an insight 
# into the bots trading activity and for debugging

import datetime, os

from TradingBot.Portfolio import Portfolio
from Util.DateHelper import DateHelper

# Potential issue: see comment l37

class FileLoggertxt:
    """
    Utility class to log a snapshot of a Portfolio class to a txt file.
    The generated file is not intended for further use, but for human readability.
    """
    
    def __init__(self, prefix:str = "run", path:str = "logs") -> None:
        
        self.logFileCreated = False
        self.prefix = prefix
        self.path = path
        
        self.stockValueOnDate = 0

    def createLogFile(self):
        if not self.logFileCreated:
            print("Log file created.")
            self.dirPath = self.path
            self.fileName = self.prefix + "_" + datetime.datetime.now().strftime("%d_%b_%y_%I_%M_%p") + ".txt"
            self.log_file_created = True

    def snapshot(self, portfolio: Portfolio, mode: int, date: datetime = None) -> None:
        """Updates the TXT file log associated with this instance of the FileLoggerTXT

        Args:
            portfolio (Portfolio): Portfolio to write the log for
            mode (int, optional): Bot mode
            date (datetime): date to use for logging.
        """
        filePath = os.path.join(self.dirPath, self.fileName)
        
        self.stockValueOnDate = 0
        
        with open(filePath, mode="a") as log:
            log.write(f"date: {DateHelper.format(date)}\n")
            log.write(f"funds in portfolio: ${portfolio.funds}\n\n")
            log.write("stocks held in portfolio: \n")
        
            for stock in portfolio.getStocks():
                log.write(f"{stock.ticker} ")
                log.write(f"amount of stock: {stock.amount}\n")
                
                if mode == 0:
                    stockValue = stock.amount * stock.getPrice()
                
                elif mode == -1:
                    #check to ensure no None prices cause an error
                    stockValue = stock.getPrice(-1, date)
                    if stockValue is None: stockValue = 0
                    stockValue = stock.amount * stockValue
                    self.stockValueOnDate += stockValue
                
                log.write(f"value of stock: ${stockValue}\n \n")
            
            # Does this work as intended? Pay attention to Scope of stockValue, maybe an issue
            log.write(f"Overall profit/loss: ${portfolio.funds + self.stockValueOnDate - portfolio.startingFunds}\n")     
            log.write("\n")   
       
        

        
            
        

