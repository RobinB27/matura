# This file implements the Graphing class, mainly using matplotlib.
# The Graphing class handles the production of all visualisations.
# Visualisations currently implemented are a graph showing the change in value of the portfolio over time
# and a graph showing the changes in the stocks held in a portfolio over time.
# The methods starting with 'fetch' or 'parse' are used for reading a log file
# and getting the necessar data from it and converting it into a format usable by matplotlib.

import json, datetime
import matplotlib.pyplot as plt


class Graphing:
    """
        Provides tools to visualise JSON logs produced by Bot runs using matplotlib.
    """
    dateFormat = "%Y-%m-%d"
        
    def plotComposition(path: str, displayWindow: bool = False, savePath: str = "output/") -> None:
        """Generates a plot visualising portfolio compositon changes over time.

        Args:
            path (str): path to the JSON log file
        """
        x, y = Graphing.parseForComp(path)
        name = "Portfolio over Time" + "_" + datetime.datetime.now().strftime("%d_%b_%y_%I_%M_%p")
        
        plt.title(name)
        plt.xlabel("Days")
        plt.ylabel("Stocks held")
        
        for ticker, amounts in y.items():
            # Plot config
            plt.plot(x, amounts, label=ticker)
        
        plt.legend()
        
        if displayWindow: plt.show()
        if savePath is not None: plt.savefig(savePath + name + ".png", dpi=300)
    
    def parseForComp(path: str) -> tuple[list, dict]:
        """Utility funcion for getting x & y values for a time/composition graph from a log file.
        
        Args:
            path (str): path to the JSON log file
        Returns:
            list, list: x-value list, dict containing stock amount lists (y values)
        """
        data = Graphing.fetchLog(path)
        
        # x & y for plot
        dates = []
        amounts ={} # dict containing lists of y-values for all stocks
        
        # extract stock names from first snapshot
        for stock in data["snapshots"][0]["stocksHeld"]: amounts[stock["name"]] = []
        
        prevDate = None
        daysPassed = 0
        for snapshot in data["snapshots"]:
            # Getting y values (stocks held)
            for stock in snapshot["stocksHeld"]: amounts[stock["name"]].append(stock["amount"])
            
            # Getting x values (time)
            if prevDate is None:
                dates.append(0)
                prevDate = Graphing.strToDate(snapshot["date"])
            else:
                currentDate = Graphing.strToDate(snapshot["date"])
                difference = currentDate - prevDate
                difference = difference.days
                daysPassed += difference
                dates.append(daysPassed)
                prevDate = currentDate
        
        return dates, amounts

    def plotValue(path: str, displayWindow: bool = False, savePath: str = "output/") -> None:
        """Generates a plot visualising portfolio value development over time.\n

        Args:
            path (str): path to the JSON log file
        """
        x, y = Graphing.parseForValue(path)
        name = "Value over Time" + "_" + datetime.datetime.now().strftime("%d_%b_%y_%I_%M_%p")
        
        # Plot config
        plt.title(name)
        plt.plot(x, y)
        plt.xlabel("Days")
        plt.ylabel("Portfolio value")
        
        if displayWindow: plt.show()
        if savePath is not None: plt.savefig(savePath + name + ".png", dpi=300)
        
    def fetchLog(path: str) -> dict:
        """Utility function for file handling

        Args:
            path (str): path to the JSON log file
        Returns:
            dict: processed JSON log file
        """
        try:
            with open(path, "r") as log: return json.load(log)
        except FileNotFoundError as error:
            print("Invalid path entered during Graph creation, file could not be found.")
            raise error
                
    def parseForValue(path: str) -> tuple[list, list]:
        """Utility funcion for getting x & y values for a time/value graph from a log file.

        Args:
            path (str): path to the JSON log file
        Returns:
            list, list: x-value list, y-value list
        """
        data = Graphing.fetchLog(path)
        
        # x & y for plot
        dates = []
        values =[]
        
        prevDate = None
        daysPassed = 0
        for snapshot in data["snapshots"]:
            # Getting y values (value of portfolio)
            portfolioValue = snapshot["funds"]
            # value Attribute already represents value of all stocks of this type, not individual stock price
            for stock in snapshot["stocksHeld"]: portfolioValue += stock["value"]
            values.append(portfolioValue)
            
            # Getting x values (time)
            if prevDate is None:
                dates.append(0)
                prevDate = Graphing.strToDate(snapshot["date"])
            else:
                currentDate = Graphing.strToDate(snapshot["date"])
                difference = currentDate - prevDate
                difference = difference.days
                daysPassed += difference
                dates.append(daysPassed)
                prevDate = currentDate
        
        return dates, values
        
    def strToDate(dateStr:str) -> datetime.date: 
        """Shorthand for string to date conversion used often in this module. 

        Args:
            string (str): String in format descirbed in Graphing.dateFormat
        Returns:
            datetime.date: converted date
        """
        # Courtesy of https://stackoverflow.com/questions/2803852/python-date-string-to-date-object
        return datetime.datetime.strptime(dateStr, Graphing.dateFormat).date()