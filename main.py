# This file acts as the main entrance point for the entire programme
#
# It allows both running individual bot runs and test cycles using command line arguments.
# If no arguments are provided, a simple CLI is started, which gets the required parameters through user input.
# 
# Additionally, all functionality in this repository may also be used as a library. I.e. bot runs can be done
# simply by importing TradingBot.Bot and manually defining a new bot and starting it.
# Similarly, the DataGen module can be accessed by simply importing DataGen.Testing and calling
# any of the desired testing functions included in it.

import sys, ast
from datetime import datetime

from TradingBot.Bot import Bot
from TradingBot.SimpleSentimentDM import SimpleSentimentDM
from TradingBot.AvgSentimentDM import AvgSentimentDM
from TradingBot.MACDDM import MACDDM
from TradingBot.BuyAndHoldDM import BuyAndHoldDM
from DataGen.Testing import Testing

stratTable = {
    "0": None,
    "1": SimpleSentimentDM,
    "2": AvgSentimentDM,
    "3": MACDDM,
    "4": BuyAndHoldDM
}

stratTableStr = {
    "SimpleSentiment": SimpleSentimentDM,
    "AverageSentiment": AvgSentimentDM,
    "MACD": MACDDM,
    "BuyAndHold": BuyAndHoldDM
}

def CLI() -> None:
    """
    Gets user input through a command line interface, which guides the user through the bot / testing tool setup.\n
    This is run by the main function if no command line arguments are given / if the main file was not opened through the console.

    Raises:
        SyntaxError: May be raised if arguments given don't fit the format that has been asked for
    """
    print("Please select a tool: Bot run (1) or Testing utility (2)")
    response = int(input("Tool:\t"))
        
    if response == 1:
        # Bot setup
            
        # mode selection
        print("Please select a bot mode: Historical data mode (1) or realtime mode (2)")
        mode = int(input("Mode:\t"))
            
        # Strategy selection
        print("Please select a trading strategy:\n(1) Simple Sentiment Strategy\n(2) Average Sentiment Strategy\n(3) MACD Strategy\n(4) Buy and Hold Strategy")
        strat: int = int(input("Strategy: "))
        if strat < 1 or strat > 4: raise SyntaxError("Invalid argument passed. Please enter either 1, 2 or 3")
        strat: object = stratTable[str(strat)]
            
        # Mode specific queries
        date = None
        if mode == 1:
            # Internally -1 is used, 1 is used to simplify user interction
            mode = -1
            print("Please select a starting date in format DD-MM-YYYY")
            print("\tMaximum date: 11-06-2020\n\tMinimum date: 01-01-2011")
            date = str(input("Date:\t"))
            # Raises error if format is incorrect
            date = datetime.strptime(date, "%d-%m-%Y")
        elif mode == 2: 
            # Internally 0 is used, 2 is used to simplify user interaction
            mode = 0
        else: raise SyntaxError("Invalid argument passed. Please enter either 1 or 2")
            
        # start bot
        testBot = Bot(strat(mode), date, mode)
        testBot.initialiseCLI()
        testBot.start()
            
    elif response == 2: Testing.CLI()
    else: raise SyntaxError("Invalid argument passed. Please enter either 1 or 2")

def main() -> None:
    """
    Main function of the programme.\n
    It allows both running individual bot runs and test cycles using command line arguments.\n
    If no arguments are provided, a simple CLI is started, which gets the required parameters through user input.
    """
    
    # 1 means only the file name was passed, launches CLI
    if len(sys.argv) == 1: CLI()
    else:
        # Parse args
        args = sys.argv
        tool = args[1]
        # Check tool validity
        if tool != "run" and tool != "test" and tool != "help":
            raise SyntaxError("Invalid tool selected, first argument must either be 'run', 'test' or 'help'.")
        params = args[2:]
        
        if len(params) % 2 != 0: raise SyntaxError("Invalid number of parameters")
        params = [[params[2*i], params[2*i+1]] for i in range(len(params) // 2)]
        
        # Syntax: fileName run -m <mode> -s <strategyDM> -d <startDate DDMMYYYY> -f <funds> -l <stockList> -p <timePeriod> -i <interval> -a <intervalAmount>
        # collect input
        options = {
            "mode": None,
            "DMs": [],
            "funds": None,
            "stockList": [],
            "timePeriod": None,
            "startDate": None,
            "interval": None,
            "intervalCount": None,
            "runs": None
        }
        # Parse all params, check their validity and add to options dict
        # Only check validity required for both run and test tool, specific validity checks are done later
        for param in params:
            # General run params
            if param[0] == "-m" or param[0] == "--mode": 
                # set mode int to what is used internally, check validity
                options["mode"] = int(param[1])
                if options["mode"] == 1: options["mode"] = -1
                elif options["mode"] == 2: options["mode"] = 0
                else: raise SyntaxError("Invalid bot mode given, must be either 1 (historical data) or 2 (realtime).")
                
            elif param[0] == "-s" or param[0] == "--strategy": 
                # converted to class using dict[str] -> class
                options["DMs"].append(param[1])
           
            elif param[0] == "-f" or param[0] == "--funds": 
                # Check validity
                options["funds"] = int(param[1])
                if options["funds"] < 0: raise SyntaxError("Funds can't be below 0")
                
            elif param[0] == "-l" or param[0] == "--list": 
                options["stockList"].append(param[1])

            elif param[0] == "-p" or param[0] == "--period": 
                options["timePeriod"] = int(param[1])
                if options["timePeriod"] < 0: raise SyntaxError("Period can't be below 0")
                
            # Historical mode bot params
            elif param[0] == "-d" or param[0] == "--date": options["startDate"] = datetime.strptime(param[1], "%d%m%Y")
            
            # Realtime mode bot params
            elif param[0] == "-i" or param[0] == "--interval": 
                options["interval"] = int(param[1])
                if options["interval"] < 0: raise SyntaxError("interval can't be below 0")

            elif param[0] == "-c" or param[0] == "--intervalCount": 
                options["intervalCount"] = int(param[1])
                if options["intervalCount"] < 0: raise SyntaxError("intervalCount can't be below 0")
                
            # testing specific params
            elif param[0] == "r" or param[0] == "--runs": 
                options["runs"] = int(param[1])
                if options["runs"] < 0: raise SyntaxError("runs count can't be below 0")
        
        # Initiatie all strategies
        if tool == "test": options["mode"] = -1
        for i in range(len(options["DMs"])):
            strat = options["DMs"][i]
            if strat in stratTableStr: 
                strat = stratTableStr[strat](options["mode"])
                options["DMs"][i] = strat 
            else: raise SyntaxError(f"Strategy {strat} is not a valid strategy. Please use SimpleSentiment, AverageSentiment, MACD or BuyAndHold")
        
        if tool == "run":
            print(options)
            # run tool specific validity check
            
            # Check if all required params are present
            if options["mode"] == None: raise SyntaxError("Bot mode (-m, --mode) is required for tool 'run'.")
            elif options["funds"] is None: raise SyntaxError("funds (-f, --funds) is requird for tool 'run'.")
            elif options["stockList"] is None: raise SyntaxError("Stock list (-l, --list) is required for tool 'run'.")
            
            # Check if all mode-specific params are present
            if options["mode"] == -1:
                if options["timePeriod"] is None: raise SyntaxError("Period (-p, --period) is required for tool 'run'.")
            elif options["mode"] == 0:
                if options["interval"] is None: raise SyntaxError("Interval (-i, --interval) is required for tool 'run'.")
                elif options["intervalCount"] is None: raise SyntaxError("IntervalCount (-c, --intervalCount) is required for tool 'run'.")
            
            # Check if exactly one strategy is given
            if len(options["DMs"]) == 0: raise SyntaxError("A strategy (-s, --strategy) is required for tool 'run'.")
            elif len(options["DMs"]) > 1: raise SyntaxError("Only one strategy can be used for tool 'run'.")
            
            # launch bot run
            bot = Bot(options["DMs"][0], options["startDate"], options["mode"])
            # Bot mode is valid, already tested
            # Needs seperate initialise syntax
            if options["mode"] == -1:
                bot.initialise(options["funds"], options["stockList"], options["timePeriod"])
            else:
                bot.initialise(options["funds"], options["stockList"], options["intervalCount"], options["interval"])
            bot.start()
            
        elif tool == "test":
            # test tool specific validity check
            if options["runs"] is None: raise SyntaxError("runs (-r, --runs) is required for tool 'test'.")
            if len(options["DMs"]) == 0: raise SyntaxError("At least one strategy (-s, --strategy) is required for tool 'test'.")

            # inform user about defaults if left blank
            if options["funds"] is None: print("funds set to default value: 1000")
            if options["startDate"] is None: print("startDate set to default: Randomized")
            if options["timePeriod"] is None: print("period set to default constraints: (10, 50)")
            if options["stockList"] == []: print("stockList set to default: Randomized")
            
            # launch Test run
            Testing.compareDMs(options["runs"], options["DMs"], options["funds"], options["startDate"], options["stockList"], options["timePeriod"])
          
        elif tool == "help":
            # print command list
            with open("Util/mainHelp.txt") as file: print(file.read())

# main idiom
if __name__ == '__main__': main()