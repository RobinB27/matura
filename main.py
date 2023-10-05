# This file acts as the main entrance point for the entire programme
#
# It allows both running individual bot runs and test cycles using command line arguments.
# If no arguments are provided, a simple CLI is started, which gets the required parameters through user input.
# 
# Additionally, all functionality in this repository may also be used as a library. I.e. bot runs can be done
# simply by importing TradingBot.Bot and manually defining a new bot and starting it.
# Similarly, the DataGen module can be accessed by simply importing DataGen.Testing and calling
# any of the desired testing functions included in it.

import sys
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

def main() -> None:
    """
    Main function of the programme.\n
    It allows both running individual bot runs and test cycles using command line arguments.\n
    If no arguments are provided, a simple CLI is started, which gets the required parameters through user input.
    """
    
    # 1 means only the file name was passed
    if len(sys.argv) == 1:
        # Ask for user input with CLI
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
        
    else:
        # Parse args
        args = sys.argv
        raise NotImplementedError("Console arg parsing not implemented.")

if __name__ == '__main__': main()