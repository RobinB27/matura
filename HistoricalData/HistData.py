# This file implements the HistData class (Historical Dataset)
# This class is needed to allow the bot to interact with a large dataset of headlines from the past ~10 years.
# The dataset used can be found here: https://www.kaggle.com/datasets/miguelaenlle/massive-stock-news-analysis-db-for-nlpbacktests
# The dataset is no longer included in this project due to its large file size preventing us from incorporating it into the GitHub repository.
# The function 'convertData()' was used to convert the dataset into the two JSON files data1.json & data2.json, it requires the original dataset to be installed to function.
# The dataset has been split into 2 JSON files using 'splitData()' so as to circumvent the 100mb filesize limit on free GitHub repositories. Besides this
# the splitting serves no further use and the bot would work identically with just one JSON file.

import csv, json, datetime


class HistData():
    """
    Provides quick access to the historical dataset.\n
    News can be accessed by date and Ticker.\n
    Example:\n
    HistData.getHeadlinesSTR("2020-12-22", "TSLA") -> [{"text"="Some Headline", "date"="2020-12-22", "ticker"="TSLA"}, {...}]
    """
    dataDict = None
    pathsJSON = ["HistoricalData/data.json", "HistoricalData/data1.json", "HistoricalData/data2.json"]
    pathCSV = "HistoricalData/analyst_ratings_processed.csv"
    
    
    def getData() -> dict:
        """Use this function to access the usable dict of the dataset. This function ensures the file must only be read once.

        Returns:
            dict: Dict of the historical dataset, keys are dates in "YYYY-MM-DD", values are Lists of all related headlines. (each represented as dicts containing text, date & ticker)
            Example: dict[2020-08-20] -> [{"text": "some Headline", "date": "2020-08-20", "ticker": "TCKR"}]
        """
        if HistData.dataDict == None: HistData.dataDict = HistData.readData()
        return HistData.dataDict
    
    def getHeadlinesDT(date: datetime.date, ticker: str = None) -> list[dict]:
        """Returns a list of all headlines published on the specified date. Takes a datetime.date object instead of a string.

        Args:
            date (date): a date object from datetime.date
            ticker (str, optional): Stock ticker as string if filtering by Ticker is desired. Defaults to None

        Returns:
            list[dict]: List of all headlines, each in dict form ("text", "date" & "ticker" attributes). Returns -1 if no headlines were found.
        """
        date = date.strftime("%Y-%m-%d")
        return HistData.getHeadlinesSTR(date, ticker)
    
    def getHeadlinesSTR(date: str, ticker: str = None) -> list[dict]:
        """Returns a list of all headlines published on the specified date. Takes a string instead of a datetime.date object

        Args:
            date (str): "YYYY-MM-DD" format date string
            ticker (str, optional): Stock ticker as string if filtering by Ticker is desired. Defaults to None

        Returns:
            list[dict]: List of all headlines, each in dict form ("text", "date" & "ticker" attributes). Returns -1 if no headlines were found.
        """
        data = HistData.getData()
        
        if date in data and ticker is None:
            return data[date]
        elif date in data and ticker is not None:
            headlines: list = data[date]
            for i, headline in enumerate(headlines):
                if headline.ticker != ticker: headlines.pop(i)
            return headlines if len(headlines) > 0 else -1 
        else: return -1
    
    
    def getHeadlinesRange(date1: datetime.date, date2: datetime.date, ticker: str = None) -> list[dict]:
        """Get all headlines between 2 dates. (dates inclusive)

        Args:
            date1, date2 (datetime.date): start and end dates
            ticker (str, optional): Stock ticker as string if filtering by Ticker is desired. Defaults to None

        Raises:
            Exception: To prevent an infinite while loop the date traversal stops at a specified limit.

        Returns:
            list[dict]: List of all headlines, each in dict form ("text", "date" & "ticker" attributes). Returns -1 if no headlines were found.
        """
        # Organise dates
        past, present = None
        if date1 < date2: past, present = date1, date2
        else: past, present = date2, date1
        
        # Traverse
        headlines = []
        limit, counter = 100, 0
        while present != past:
            headlines += HistData.getHeadlinesDT(present)
            present -= datetime.timedelta(days=1)
            
            if counter == limit: 
                raise Exception("Limit of days reached while fetching headlines.\nThe dates entered may be incorrect.\nIncrease limit if this is intentional behaviour.")
            limit += 1
            
        return headlines if len(headlines) > 0 else -1 
    
    def readData() -> dict:
        """Reads the usable dict of the historical dataset stored in data.json. Only intended for use in getData().
        
        Raises:
            FileNotFoundError: If data.json isn't present, try generating it with HistData.convertData()

        Returns:
            dict: Dataset dictionary from data.json, as prepared in HistData.convertData().
        """
        try:
            logs = []
            for i in range(2):
                with open(HistData.pathsJSON[1 + i], 'r') as log: 
                    log = json.loads(log.read());
                    logs.append(log)
            # Dict merge operator (https://peps.python.org/pep-0584/)
            data = logs[0] | logs[1]
            return data
                    
        except FileNotFoundError as error:
            print("data.json could not be read, it may not have been made yet. \nUse HistData.convertData() to create data.json")
            raise error
        
    def splitdata() -> None:
        """
        Splits data.json into 2 files which are each <100mb, circumventing Githubs 100mb filesize hardlimit on public repos
        """
        # Idea courtesy of https://stackoverflow.com/questions/12988351/split-a-dictionary-in-half
        
        data = HistData.getData()
        items = list(data.items())
        
        split = int(len(data) * 0.75)
        
        halves = [dict(items[split//2:]), dict(items[:split//2])]
        
        for i, d in enumerate(halves):
            content = json.dumps(d)
            try:
                with open(HistData.pathsJSON[1 + i], "w") as log: log.write(content)
            except FileNotFoundError as error:
                print("data1.json or data.2json could not be found. They might not exist.")
                raise error
    
    def convertData(showCorrections = False) -> None:
        """
        Reads the historical dataset and writes a usable dict to data.json.\n
        Do not use if data.json has already been generated as this takes time.
        """
        try:
            # Non-utf8 encoding raises exception, don't remove
            dates = {}
            with open(HistData.pathCSV, newline='', encoding="utf8") as csvfile:
                # Reading file takes about a minute with console logging so this message should be useful
                print("Converting dataset to JSON, this may take a while.")
                reader = csv.reader(csvfile, delimiter=',')
                
                firstRow = True
                prevRow = None
                for row in reader:
                    # row is str list, 0 = index, 1 = headline, 2 = date, 3 = Ticker / Length is NOT always 4
                    if firstRow:
                        # skip first line, csv column names
                        firstRow = False
                    else:
                        # Some rows in the dataset are faulty and split on two rows, this recombines these lines
                        if len(row) != 4: 
                            if prevRow == None: 
                                prevRow = row
                                continue
                            else:
                                # first element useless
                                row = prevRow + row[1:]
                                prevRow = None
                                if showCorrections: print("CORRECTION MADE: ", row)
                        
                        # date is in YYYY-MM-DD
                        date = row[2].split(" ")[0]
                        headline = {
                            "text": row[1],
                            "date": date,
                            "ticker": row[3]
                        }
                        
                        if date in dates:
                            dates[date].append(headline)
                        else:
                            dates[date] = [headline]
            
            try:
                # Write to JSON file
                content = json.dumps(dates)
                with open(HistData.pathsJSON[0], "w") as log: log.write(content)
                print("Conversion finished.")
                    
            except FileNotFoundError as error:
                print("Dataset was read but could not be written to data.json, The file might not exist.")
                raise error

        except FileNotFoundError as error:
            print("Dataset could not be openened. The function may not have been called from a main file.")
            raise error