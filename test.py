from HistoricalData.HistData import HistData
from datetime import datetime, timedelta

date = datetime(2019, 1, 1)

for i in range(300):
    print(HistData.getHeadlinesDT(date, "TSLA"))
    date += timedelta(days=1)