from bs4 import BeautifulSoup
from WebScraping.YahooFinance.Headline import Headline


def parseHTML(pageSource) -> list[Headline]:
    """ Returns an array of Headline Objects with headline, date, source """
    soup = BeautifulSoup(pageSource, 'html.parser')

    # Gather all news items
    listElements = soup.find_all("li", {
        "class": ["js-stream-content", "Pos(r)"]
    })

    headlineArray = []
    for li in listElements:
        div1 = li.findChildren("div", recursive=False)

        # Skip iteration if element is an ad
        if "gemini-ad" in div1[0]['class']: continue

        # Retrieve content from li elements
        try:
            spans = li.div.div.findAll('span')
            h3s = li.div.div.findAll('h3')

            headline = h3s[0].text
            source = spans[0].text
            date = spans[1].text

            headlineArray.append(Headline(headline, date, source))

        except: print("Error in headline lookup")

    return headlineArray


def parseHTMLsimple(pageSource) -> list[str]:
    """ Returns an array of headlines as strings. """

    soup = BeautifulSoup(pageSource, 'html.parser')
    headlineElements = soup.findAll(class_="js-content-viewer")

    headlines = []
    for elem in headlineElements:
        headlines.append(elem.text)

    return headlines
