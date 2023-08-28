# This file implements the Headline class
# This class represents the data format in which the WebScraper class provides headlines.

class Headline:
    def __init__(self, text, date="unknown", source="unknown"):
        self.text = text
        self.date = date
        self.source = source
