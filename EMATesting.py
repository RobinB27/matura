import yfinance as fy
import pandas as pd
from decimal import *

from datetime import datetime, timedelta, date
from TradingBot.Portfolio import Portfolio

from TradingBot.FinancialCalculators.SMACalculator import SMACalculator

from diskcache import Cache

from Util.Config import Config



prices = [11.05, 11.75, 12.25, 14, 16, 17, 15.6, 15.75, 16, 14, 16.5, 17, 17.25, 18, 18.75,
20 ]
days = 5

ema_values = []
ema_yesterday = prices[0]  # Start with the first price as EMA(yesterday)

alpha = 2 / (1 + days)



for price in prices:
    ema_today = (price * alpha) + (ema_yesterday * (1 - alpha))
    ema_values.append(ema_today)
    ema_yesterday = ema_today

for i in range(len(ema_values)):
    to_print = round(Decimal(ema_values[i]), 2)
    print(f"{to_print}", flush=True)