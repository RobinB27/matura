import yfinance as fy
from datetime import datetime, timedelta, date
import pandas as pd
from TradingBot.Portfolio import Portfolio

class MACDDecisionMaking:
    
    
    def __init__(self, mode: int = 0):
        
        self.mode = mode
        
    
    def makeStockDecision(self, portfolio, ticker: str, mode: int = 0, dateStart: str = "0"):
        """makes a decision whether to buy a stock or not on a given date

        Args:
            portfolio (_type_): _description_
            ticker (str): _description_
            mode (int, optional): _description_. Defaults to 0.
            dateStart (str, optional): _description_. Defaults to "0".

        Returns:
            decision in a binary format where 0 is no and 1 is yes
        """
        #TO DO CHECK IF TICKER VALID AT START
        decision = 0
        #EMA = (todays MACD * K) + (Previous EMA * (1 – K))
        
        signalLine = 0
        weightMultiplier = 2 / (9 + 1)
        
        MACDPlaceholder = 0
        if mode == 0:
            MACDPlaceholder = self.calculateMACD(portfolio, ticker)
            print(f"MACD: {MACDPlaceholder}")
            
            MACDAverage = 0
            placeHolderDate = date.today()
            
            executions = 0
            while executions < 9:
                placeHolderDate = placeHolderDate - timedelta(days=1)
                if placeHolderDate.isoweekday() > 5:
                    continue
                
                placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                MACDAverage += self.calculateMACD(portfolio, ticker, -1, placeHolderDate)
                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                executions += 1
            
            MACDAverage = MACDAverage / 9

            signalLine = (MACDPlaceholder * weightMultiplier) + (MACDAverage * (1 - weightMultiplier))
            print(f"SIgnal line: {signalLine}")
            
        elif mode == -1:
            FirstCheckPlaceholder1 = datetime.strptime(dateStart, "%Y-%m-%d")
                
            if FirstCheckPlaceholder1.isoweekday() > 5:
                    print(f"Weekend: {FirstCheckPlaceholder1}")
                    exit()
            
            FirstCheckPlaceholder2 = FirstCheckPlaceholder1
            FirstCheckPlaceholder2 += timedelta(days=1)
            
            FirstCheckPlaceholder1 = FirstCheckPlaceholder1.strftime("%Y-%m-%d")
            FirstCheckPlaceholder2 = FirstCheckPlaceholder2.strftime("%Y-%m-%d")
            
            for stock in portfolio.stocksHeld:
                if stock.name == ticker:
                    if stock.getStockPrice(-1, FirstCheckPlaceholder1, FirstCheckPlaceholder2) is None:
                                print(f"exception date: {FirstCheckPlaceholder1}")
                                exit()
                                
            MACDPlaceholder = self.calculateMACD(portfolio, ticker, -1, dateStart)
            print(f"MACD: {MACDPlaceholder}")
            
            MACDAverage = 0
            placeHolderDate = datetime.strptime(dateStart, "%Y-%m-%d")
            
            executions = 0
            while executions < 9:
                
                check = False
                
                placeHolderDate = placeHolderDate - timedelta(days=1)
                
                getStockPricePlacholder = placeHolderDate
                getStockPricePlacholder += timedelta(days=1)
                getStockPricePlacholder = getStockPricePlacholder.strftime("%Y-%m-%d")
                
                if placeHolderDate.isoweekday() > 5:
                    print(f"Weekend: {placeHolderDate}")
                    continue
                placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        if stock.getStockPrice(-1, placeHolderDate, getStockPricePlacholder) is None:
                                print(f"exception date: {placeHolderDate}")
                                check = True
                                continue
                            
                if check == True:
                    placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                    continue
                                
                MACDAverage += self.calculateMACD(portfolio, ticker, -1, placeHolderDate)
                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                executions += 1
            
            MACDAverage = MACDAverage / 9

            signalLine = (MACDPlaceholder * weightMultiplier) + (MACDAverage * (1 - weightMultiplier))
            print(f"SIgnal line: {signalLine}")
            print(MACDPlaceholder)
        
        if MACDPlaceholder > signalLine:
            decision = 1
        elif MACDPlaceholder < signalLine:
            decision = 0
        
        return decision
    
    def calculateMACD(self, portfolio, ticker: str, mode: int = 0, dateStart: str = "0"):
        
        # MACD = 12 day EMA - 26 day EMA
        # EMA = exponential moving average
        
        # thought that maybe two modes arent needed because the code in mode = 0 should work for every date given (needs testing)
        # the above thought isnt possible due to the way the getStockPrice() function is implemented
        
        # mode is currently using the function param mode, shouldn't this be the class variable?
        
        if mode == 0:
            
            EMA_Placeholder12days = self.calculateEMA(12, portfolio, ticker)
            EMA_Placeholder26days = self.calculateEMA(26, portfolio, ticker)

            MACDline = EMA_Placeholder12days - EMA_Placeholder26days
            return MACDline
            
            
            
        elif mode == -1:
            
            
            
            EMA_Placeholder12days = self.calculateEMA(12, portfolio, ticker, -1, dateStart)
            EMA_Placeholder26days = self.calculateEMA(26, portfolio, ticker, -1, dateStart)

            
            MACDline = EMA_Placeholder12days - EMA_Placeholder26days
            return MACDline

     
    #lot of boilerplate can be removed by putting the while loop inside it's own function
    def calculateSMA(self, daysToCalculate: int, portfolio, ticker, mode = 0, dateToCalculate = "0"):
        """calculates the SMA of a stock, variable time period, mode 0 for current time, mode -1 for past prices

        Args:
            daysToCalculate (int): _description_
            portfolio (_type_): _description_
            ticker (_type_): _description_
            mode (int, optional): _description_. Defaults to 0.
            dateToCalculate (str, optional): _description_. Defaults to "0".

        Returns:
            _type_: _description_
        """
        
        SMA_Value = 0
        
        if mode == 0:
            startDate = date.today()
            #checks if the called date is a weekend or a holiday
            if startDate.isoweekday()  > 5:
                print("It's the weekend no current stock prices available to buy")
                exit()
            
        
            #should output the SMA value for avariable number of days
            for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        #checks if the stockmarket is open yet
                        #this has the potential to get buggy/confusing if the day is a holiday since it will never open
                        if stock.getStockPrice() is None:
                            print("no stock price available yet")
                            exit()
                        #adds the current price to the SMA_Value  
                        else:   
                            SMA_Value +=  stock.getStockPrice()
                            placeHolderDate = startDate - timedelta(days=1)
                        #iterates over the past stock prices and adds the closing stock price to the SMA claculation from the current date backwards 
                        
                        
                        executions = 0
                        while executions != daysToCalculate - 1:
                            
                            #checks if date is a weekend, meaning no price
                            if placeHolderDate.isoweekday() > 5:
                                placeHolderDate -= timedelta(days=1)
                                print(f"Weekend on: {placeHolderDate}")
                                continue
                            if stock.getStockPrice(-1, placeHolderDate) is None:
                                placeHolderDate -= timedelta(days=1)
                                print("exception date")
                                continue
                                
                            else:
                                
                                secondplaceHolderDate = placeHolderDate + timedelta(days=1)
                            
                                #converts the datetime objects into str format for getStockPrice()
                                placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                                secondplaceHolderDate = secondplaceHolderDate.strftime("%Y-%m-%d")
                                
                                #check if the stockmarket is open on that day (holiday check)
                                if stock.getStockPrice(-1, placeHolderDate, secondplaceHolderDate) is None:
                                    placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                                    placeHolderDate -= timedelta(days=1)
                                    continue
                                
                                SMA_Value +=  stock.getStockPrice(-1, placeHolderDate, secondplaceHolderDate)
                                
                                #converts the str back into datetime objects
                                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                                secondplaceHolderDate = datetime.strptime(secondplaceHolderDate, "%Y-%m-%d") #not sure if line is needed, to test
                                
                                placeHolderDate -= timedelta(days=1)
                            executions += 1
                          
                        #divides the total value by number of days to get the SMA
                        SMA_Value = SMA_Value / daysToCalculate
                        return SMA_Value
                
        elif mode == -1:
            
            for stock in portfolio.stocksHeld:
                    if stock.name == ticker:
                        
                        executions = 0
                        placeHolderDate = datetime.strptime(dateToCalculate, "%Y-%m-%d")
                        
                        while executions < daysToCalculate:
                            
                            #checks if date is a weekend, meaning no price
                            #DOESNT WORK
                            if placeHolderDate.isoweekday() > 5:
                                placeHolderDate -= timedelta(days=1)
                                continue
                            
                            #creates the second date needed for the getStockPrice function
                            getStockPricePlacholder = placeHolderDate
                            getStockPricePlacholder += timedelta(days=1)
                            
                            
                            placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                            getStockPricePlacholder = getStockPricePlacholder.strftime("%Y-%m-%d")
                            
                            if stock.getStockPrice(-1, placeHolderDate, getStockPricePlacholder) is None:
                                
                                placeHolderDate =  datetime.strptime(placeHolderDate, "%Y-%m-%d")
                                placeHolderDate -= timedelta(days=1)
                                print("exception date")
                                continue
                            
                            placeHolderDate =  datetime.strptime(placeHolderDate, "%Y-%m-%d")   
                        
                            secondplaceHolderDate = placeHolderDate + timedelta(days=1)
                            
                            #converts the datetime objects into str format for getStockPrice()
                            placeHolderDate = placeHolderDate.strftime("%Y-%m-%d")
                            secondplaceHolderDate = secondplaceHolderDate.strftime("%Y-%m-%d")
                                
                            #check if the stockmarket is open on that day (holiday check)
                            if stock.getStockPrice(-1, placeHolderDate, secondplaceHolderDate) is None:
                                placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                                placeHolderDate -= timedelta(days=1) 
                                continue
                                
                            SMA_Value +=  stock.getStockPrice(-1, placeHolderDate, secondplaceHolderDate)
                                
                            #converts the str back into datetime objects
                            placeHolderDate = datetime.strptime(placeHolderDate, "%Y-%m-%d")
                            secondplaceHolderDate = datetime.strptime(secondplaceHolderDate, "%Y-%m-%d") #not sure if line is needed, to test
                                
                            placeHolderDate -= timedelta(days=1)
                            executions += 1
                          
                        #divides the total value by number of days to get the SMA
                        SMA_Value = SMA_Value / daysToCalculate
                        return SMA_Value
        
                        
                        
    def calculateEMA(self, daysToCalculate: int, portfolio, ticker, mode = 0, dateToCalculate = "0"):
        """Calculates the EMA needed for MACD calculations

        Args:
            daysToCalculate (int): _description_
            portfolio (_type_): _description_
            ticker (_type_): _description_
            mode (int, optional): _description_. Defaults to 0.
            dateToCalculate (str, optional): _description_. Defaults to "0".

        Returns:
            _type_: _description_
        """
        
        #EMA(today) = (Close(today) * α) + (EMA(yesterday) * (1 - α))
        
        weightMultiplier = 2 / (daysToCalculate + 1)
        
        #could be optimised with keeping a running EMA calculation, this recalculates the EMA every time it's called
        if mode == 0:
            
            placeholderWeekendCheck = datetime.strptime(dateToCalculate, "%Y-%m-%d")
            #checks if dateToCalculate is on a weekend()
            if placeholderWeekendCheck.isoweekday() > 5:
                print("EMA calculatins not possible on a weekend")
                exit()
            
            
            EMAValue = 0
            
            SMA_Placeholder = self.calculateSMA(daysToCalculate, portfolio, ticker)
            
            stockPrice = 0
            for stock in portfolio.stocksHeld:
                if stock.name == ticker:
                    stockPrice = stock.getStockPrice()
                    
            EMAValue = (stockPrice * weightMultiplier) + (SMA_Placeholder * (1 - weightMultiplier))
            
            return EMAValue
            
        elif mode == -1:
            
            
            SMA_Placeholder = 0
            executions = 0
            
            placeHolderDate = datetime.strptime(dateToCalculate, "%Y-%m-%d")
            getStockPricePlacholder = placeHolderDate
            
            getStockPricePlacholder += timedelta(1)
            getStockPricePlacholder = getStockPricePlacholder.strftime("%Y-%m-%d")
            
            for stock in portfolio.stocksHeld:
                if stock.name == ticker:
                    SMA_Placeholder += self.calculateSMA(daysToCalculate, portfolio, ticker, -1,  dateToCalculate)

                        
            stockPrice = 0
            stockPrice = stock.getStockPrice(-1, dateToCalculate, getStockPricePlacholder)
                    
            EMAValue = (stockPrice * weightMultiplier) + (SMA_Placeholder * (1 - weightMultiplier))
           
            return EMAValue
            
        