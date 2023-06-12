from TradingBot.Portfolio import Portfolio
import json, os, datetime

# Add error handling for file handling, best practice
# Add parser

class FileLoggerJSON:
    """
    Utility class to log all contents of a portfolio class to a JSON file. \n
    Subsequent snapshots of a run are saved within the same file provided the same File Logger is used
    """
    
    def __init__(self, path: str = "logs") -> None:
        self.dirPath = path
        self.fileName = "run_" + datetime.datetime.now().strftime("%I_%M_%p_%d_%b_%y") + ".json"
    
    def snapshot(self, portfolio: Portfolio, mode:int = 0, date:str = "0") -> None:
        """
        Saves a Snapshot of portfolio to the file associated with the FileLoggerJSON instance.
        """
        filePath = os.path.join(self.dirPath, self.fileName)
        
        # Retrieve file content
        content = ""
        with open(filePath, 'r') as log: content = log.read().replace('\n', '')

        
        # If file is empty, add an empty JSON Object (json.reads() breaks on empty strings)
        if (content == ""): content = '{"snapshots": []}'
            
        # Update file content based on data in Portfolio
        content = json.loads(content);
        
        pObject = {
            "date": date,
            "name": portfolio.name,
            "funds": portfolio.funds,
            "stocksHeld": []
        }
        
        for stock in portfolio.stocksHeld:
            sObject = (
                {
                    "name": stock.name,
                    "amount": stock.amountOfStock
                    "value": "undefined"
                }
            )
            
            if mode == 0:
                value = stock.amountOfStock * stock.getStockPrice()
                
            elif mode == -1:
                placeholderDate = portfolio.addDayToDate(date)
                value = stock.amountOfStock * stock.getStockPrice(-1, date, placeholderDate)
            
            sObject["value"] = value
            
            pObject["stocksHeld"].append(sObject)
        
        content["snapshots"].append(pObject)
        
        content = json.dumps(content)
        
        # Write content to file
        with open(filePath, "w") as log: log.write(content)