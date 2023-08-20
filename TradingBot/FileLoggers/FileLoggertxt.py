from TradingBot.Portfolio import Portfolio
import datetime, os

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

    def snapshot(self, portfolio: Portfolio,  mode = 0, date: str = "0") -> None:
        filePath = os.path.join(self.dirPath, self.fileName)
        
        self.stockValueOnDate = 0
        
        with open(filePath, mode="a") as log:
            log.write(f"date: {date}\n")
            log.write(f"funds in portfolio: ${portfolio.funds}\n\n")
            log.write("stocks held in portfolio: \n")
        
            for stock in portfolio.stocksHeld:
                log.write(f"{stock.name} ")
                log.write(f"amount of stock: {stock.amountOfStock}\n")
                
                if mode == 0:
                    stockValue = stock.amountOfStock * stock.getStockPrice()
                
                elif mode == -1:
                    stockValue = stock.amountOfStock * stock.getStockPrice(-1, date)
                    self.stockValueOnDate += stockValue
                
                log.write(f"value of stock: ${stockValue}\n \n")
            
            # Does this work as intended? Pay attention to Scope of stockValue, maybe an issue
            log.write(f"Overall profit/loss: ${portfolio.funds + self.stockValueOnDate - portfolio.startingFunds}\n")     
            log.write("\n")   
       
        

        
            
        

