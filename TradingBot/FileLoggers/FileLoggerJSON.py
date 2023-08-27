from TradingBot.Portfolio import Portfolio
import json, os, datetime

# Add error handling for file handling, best practice
# Add parser

class FileLoggerJSON:
    """
    Utility class to log all contents of a portfolio class to a JSON file. \n
    Subsequent snapshots of a run are saved within the same file provided the same File Logger is used
    """
    
    def __init__(self, prefix:str = "run" ,path: str = "logs") -> None:
        self.dirPath = path
        self.fileName = prefix + "_" + datetime.datetime.now().strftime("%d_%b_%y_%I_%M_%p") + ".json"
    
    def snapshot(self, portfolio: Portfolio, mode:int = 0, date:str = "0") -> None:
        """
        Saves a Snapshot of portfolio to the file associated with the FileLoggerJSON instance.
        """
        filePath = os.path.join(self.dirPath, self.fileName)
        
        # Retrieve file content
        content = ""
        
        # If file doesn't exist yet, add empty JSON template
        try: 
            with open(filePath, 'r') as log: content = log.read().replace('\n', '')
        except FileNotFoundError:
            content = '{"snapshots": []}'
            
        # Update file content based on data in Portfolio
        content = json.loads(content);
        
        pObject = {
            "date": date,
            "funds": portfolio.funds,
            "stocksHeld": []
        }
        
        for stock in portfolio.stocksHeld:
            sObject = {
                    "name": stock.ticker,
                    "amount": stock.amount,
                    "value": "undefined"
                }
            
            if mode == 0:
                value = stock.amount * stock.getPrice()
                
            elif mode == -1:
                value = stock.amount * stock.getPrice(-1, date)
            
            sObject["value"] = value
            
            pObject["stocksHeld"].append(sObject)
        
        content["snapshots"].append(pObject)
        
        content = json.dumps(content)
        
        # Write content to file
        with open(filePath, "w") as log: log.write(content)