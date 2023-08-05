from SentimentAnalysis.Classification import getSentiment
from HistoricalData.HistData import HistData
from datetime import date

# Sentiment analysis on past events demo

sampleDate = date(2018, 11, 27)
data = HistData.getHeadlinesDT(sampleDate)

for i in range(10):
    headline = data[i]["text"]
    print("Headline:\t" + headline)
    print("Sentiment:\t" + getSentiment(headline))