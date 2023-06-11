from TradingBot.Portfolio import Portfolio

class FileLogger:
    
    #find way to name each file for the FileLogger independently,
    #meaning keep track of how many loggers there are
    #use class method for this?
    def __init__(self, name):
        self.name = name
        
        self.log = open("log.txt", mode="w")        
        

    def snapshot(self, portfolio,  mode = 0, date: str = "0"):
        with open("log.txt", mode="a") as log:
            log.write(f"date: {date}\n")
            log.write(f"funds in portfolio: ${portfolio.funds}\n")
            log.write("stocks held in portfolio: \n\n")
            for stock in portfolio.stocksHeld:
                log.write(f"{stock.name} ")
                log.write(f"amount of stock: {stock.amountOfStock}\n")
                
                if mode == 0:
                    stockValue = stock.amountOfStock * stock.getStockPrice()
                
                elif mode == -1:
                    placeholderDate = portfolio.addDayToDate(date)
                    stockValue = stock.amountOfStock * stock.getStockPrice(-1, date, placeholderDate) 
                
                log.write(f"value of stock: ${stockValue}\n \n")
            
            log.write(f"Overall profit/loss: ${portfolio.funds + stockValue}\n")     
            log.write("\n")   
       
        

        
            
        

