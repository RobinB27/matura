# "Automated Stock Trading using News Headlines"
This repository contains the source code for the matura project "Automated Stock Trading using News Headlines" developed by Robin Bacher & Lucien Gees during 2023. 
The "resultsData" folder also contains all the log data and graphs shown in the paper written for this matura project.

# Requirements
To install all the necessary dependencies, the following steps must be completed in the order shown. The program was developed using Python version 3.10.4, but newer versions should work too.
1. First, the *TA-Lib* library must be installed manually. Please refer to the operating system specific instructions listed under dependencies [here.](https://pypi.org/project/TA-Lib/)
2. Next, all other dependencies can be installed using `pip install -r requirements.txt`.
3. Finally, the specific NLTK modules required can be installed by running `py Downloads.py`.

# Usage
The bot and the testing tool can be used in multiple ways. 
1.	The *main.py* file located in the root folder of the git repository can be run from the explorer or through a terminal.
   This will launch a command line interface which guides the user through setting up a bot run or a testing cycle.
2.	When running the main.py file from the terminal, the above process can be skipped by providing the necessary arguments for either a bot run or a testing cycle using command line arguments.
   A list of all command line arguments and examples can also be accessed using `py main.py --help`
3. Bot runs and testing cycles can also be perfomed from within a script by importing *TradingBot.bot* or *DataGen.Testing*.
