from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from WebScraping.YahooFinance.Parser import parseHTML
from WebScraping.YahooFinance.Headline import Headline


class YahooWebScraper:
    """ Module to retrieve headlines from YahooFinance using Selenium & BeautifulSoup. """
    driver = None
    minElements = 20

    def getDriver():
        """ Returns webdriver, will launch the driver if it hasn't been launched yet."""

        if (YahooWebScraper.driver == None): YahooWebScraper.launchDriver()
        return YahooWebScraper.driver

    def checkIfLoaded(driver):
        """ Used in site loading. Checks whether enough relevant elements have been loaded on a site."""

        # Pages contain one additional similar element that needs to be accounted for
        minElements = YahooWebScraper.minElements + 1

        driver.execute_script("window.scrollTo(0, 10000)")
        elems = driver.find_elements(
            By.CLASS_NAME, 'StretchedBox'
        )

        if len(elems) >= minElements: return True
        else: return False

    def launchDriver():
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("start-maximised")
        options.add_experimental_option(
            "prefs",
            {"profile.managed_default_content_settings.images": 2}
        )

        driver = webdriver.Chrome(options=options)

        YahooWebScraper.driver = driver

    def closeDriver(): YahooWebScraper.driver.quit()

    def getHeadlines(ticker: str) -> list[Headline]:
        """ Returns a list of the most recent headlines on any valid stock ticker listed on YahooFinance. """
        driver = YahooWebScraper.getDriver()

        urlbase = "https://finance.yahoo.com/quote/"
        url = urlbase + ticker

        driver.get(url)
        WebDriverWait(driver=driver, timeout=5).until(
            YahooWebScraper.checkIfLoaded)

        return parseHTML(driver.page_source)
