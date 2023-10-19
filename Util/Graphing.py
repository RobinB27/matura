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
    saveFormat = "%d_%b_%y_%I_%M_%f_%p"
    timeStampFormat = "%d-%m-%y-%H-%M"
    
    def finish(displayWindow: bool, savePath: str, name: str) -> None:
        """Utility function used to display and save all Graphs regardless of plot type."""
        fig = plt.gcf()
        if savePath is not None: 
            fig.savefig(fname=savePath + name + ".png", bbox_inches='tight', dpi=300)
        if displayWindow: plt.show()
        plt.clf()
        
    def plotComposition(path: str, displayWindow: bool = False, savePath: str = "output/", customPrefix: str = None) -> None:
        """Generates a plot visualising portfolio compositon changes over time.

        Args:
            path (str): path to the JSON log file
        """
        x, y, strategy = Graphing.parseForComp(path)
        name = "Portfolio over Time" + "_" + datetime.datetime.now().strftime(Graphing.saveFormat)
        if customPrefix is not None: name = customPrefix + "_" + name
        title = "Portfolio / Time for " + strategy + " on " + datetime.datetime.now().strftime("%d. %b %Y")
        
        plt.clf()
        plt.title(title)
        plt.xlabel("Days")
        plt.ylabel("Stocks held")
        
        for ticker, amounts in y.items():
            # Plot config
            plt.plot(x, amounts, label=ticker)
        
        plt.legend()
        
        Graphing.finish(displayWindow, savePath, name)
    
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
        strategy = data["strategyName"]
        
        mode = -1 if "date" in data["snapshots"][0] else 0
        interval = data["snapshots"][0]["interval"] if "interval" in data["snapshots"][0] else None
        
        # extract stock names from first snapshot
        for stock in data["snapshots"][0]["stocksHeld"]: amounts[stock["name"]] = []
        
        prevIteration = None
        iterationsPassed = 0
        for snapshot in data["snapshots"]:
            # Getting y values (stocks held)
            for stock in snapshot["stocksHeld"]: amounts[stock["name"]].append(stock["amount"])
            
            # Getting x values (time)
            if prevIteration is None:
                dates.append(0)
                if mode == -1: prevIteration = Graphing.strToDate(snapshot["date"], mode)
                else: prevIteration = Graphing.strToDate(snapshot["timeStamp"], mode)
            else:
                if mode == -1: currentDate = Graphing.strToDate(snapshot["date"], mode)
                else: currentDate = Graphing.strToDate(snapshot["timeStamp"], mode)
                    
                difference = currentDate - prevIteration
                
                # Handle difference differently depending on mode (-1 => dates, 0 => timeStamps)
                if mode == -1:
                    difference = difference.days
                    iterationsPassed += difference
                elif mode == 0:
                    difference = difference.total_seconds() / 60
                    iterationsPassed += difference // interval
                    
                dates.append(iterationsPassed)
                prevIteration = currentDate
        
        return dates, amounts, strategy
    
    def getMode(path: str) -> int:
        """Gets the mode of a log file using its path

        Args:
            path (str): path to the file

        Returns:
            int: the bot mode used when generating that log
        """
        data = Graphing.fetchLog(path)
        return -1 if "date" in data["snapshots"][0] else 0
    
    def getInterval(path: str) -> int:
        """Gets the interval of a log file using its path

        Args:
            path (str): path to the file

        Returns:
            int: the interval used when generating that log, -1 if no interval found in log (log is likely in past mode)
        """
        data = Graphing.fetchLog(path)
        if "interval" in data["snapshots"][0]:
            return data["snapshots"][0]["interval"]
        else: return -1

    def plotValue(path: str, displayWindow: bool = False, savePath: str = "output/", customPrefix = None) -> None:
        """Generates a plot visualising portfolio value development over time.\n

        Args:
            path (str): path to the JSON log file
            displayWindow (bool): whether the graph should be displayed in a window
            savePath (str): file path for saving the graph
            customPrefix: Adds a custom prefix to the file name.
        """
        x, y, strategy = Graphing.parseForValue(path)    
        name = "Value over Time" + "_"  + datetime.datetime.now().strftime(Graphing.saveFormat)
        if customPrefix is not None: name = customPrefix + "_" + name
        title = "Value / Time for " + strategy + " on " + datetime.datetime.now().strftime("%d. %b %Y")
        
        # Plot config
        plt.clf()
        plt.title(title)
        plt.plot(x, y)
        if Graphing.getMode(path) == -1:
            plt.xlabel("Days")
        else:
            interval = Graphing.getInterval(path)
            plt.xlabel(f"Intervals, 1 interval = {interval}m")
        plt.ylabel("Portfolio value")
        
        Graphing.finish(displayWindow, savePath, name)
        
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
        
        
    def plotProfits(data: list = [], strategies:list = [], displayWindow: bool = False, savePath: str = "output/") -> None:
        bins = 20
        name = "Testing results" + "_" + datetime.datetime.now().strftime(Graphing.saveFormat)
        
        plt.clf()
        if len(strategies) > 1:
            fig, axs = plt.subplots(1, len(strategies), sharey=True, tight_layout=True)
            
            for i in range(len(strategies)):
                axs[i].hist(data[i], bins=bins)
                if len(strategies) > 2 and hasattr(strategies[i], "abbreviation"):
                    axs[i].set_title(strategies[i].abbreviation)
                else:
                    axs[i].set_title(strategies[i].__name__)
                axs[i].set_xlabel("Net profit")
                axs[i].set_ylabel("Runs")
        else:
            try:
                plt.title(strategies[0].__name__)
                plt.hist(data[0], bins=bins)
                plt.xlabel("Net profit")
                plt.ylabel("Runs")
            except:
                raise SyntaxError("Fatal error in single strategy profit graphing, probably invalid syntax")
            
        Graphing.finish(displayWindow, savePath, name)
        
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
        strategy = data["strategyName"]
        
        prevIteration = None
        iterationsPassed = 0
        # Define mode based on whether date or timestamps are used in the log
        mode = -1 if "date" in data["snapshots"][0] else 0
        # Define interval, if it exists
        interval = data["snapshots"][0]["interval"] if "interval" in data["snapshots"][0] else None
        for snapshot in data["snapshots"]:
            # Getting y values (value of portfolio)
            portfolioValue = snapshot["funds"]
            # value Attribute already represents value of all stocks of this type, not individual stock price
            for stock in snapshot["stocksHeld"]: portfolioValue += stock["value"]
            values.append(portfolioValue)
            
            # Getting x values (time), mode dependant

            # Work with dates
            if prevIteration is None:
                dates.append(0)
                if mode == -1: prevIteration = Graphing.strToDate(snapshot["date"], mode)
                else: prevIteration = Graphing.strToDate(snapshot["timeStamp"], mode)
            else:
                if mode == -1: currentDate = Graphing.strToDate(snapshot["date"], mode)
                else: currentDate = Graphing.strToDate(snapshot["timeStamp"], mode)
                    
                difference = currentDate - prevIteration
                
                # Handle difference differently depending on mode (-1 => dates, 0 => timeStamps)
                if mode == -1:
                    difference = difference.days
                    iterationsPassed += difference
                elif mode == 0:
                    difference = difference.total_seconds() / 60
                    print(difference)
                    difference = interval * round(difference / interval)
                    print(difference)
                    iterationsPassed += difference
                    
                dates.append(iterationsPassed)
                prevIteration = currentDate
                print(dates)
                print(values)
        
        return dates, values, strategy
        
    def strToDate(date:str, mode: int) -> datetime.datetime: 
        """Shorthand for string to date conversion used often in this module. 

        Args:
            string (str): String in format descirbed in Graphing.dateFormat
            mode (int): -1 converts to date, 0 converts to timeStamp
        Returns:
            datetime.datetime: converted date
        """
        # Courtesy of https://stackoverflow.com/questions/2803852/python-date-string-to-date-object
        return datetime.datetime.strptime(date, Graphing.dateFormat).date() if mode == -1 else datetime.datetime.strptime(date, Graphing.timeStampFormat)
