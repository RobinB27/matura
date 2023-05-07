from WebScraping.YahooFinance.Webscraper import YahooWebScraper

# demo

ticker = "AAPL"
headlines = YahooWebScraper.getHeadlines(ticker)

for elem in headlines:
    print("\n")
    print(elem.text)
    print("\n" + elem.date)
    print("\n" + elem.source)