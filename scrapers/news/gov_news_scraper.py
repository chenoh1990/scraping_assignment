from scrapers.scraper_interface import SeleniumScraper
from scrapers.news.news_data.data_fetcher import DataFetcher
from scrapers.news.news_data.data_saver import DataSaver
from scrapers.news.news_data.data_processor import DataProcessor


class NewsSiteScraper(SeleniumScraper):
    """
    NewsSiteScraper uses Selenium to scrape news_data from a news website.
    """
    def __init__(self, url: str):
        super().__init__(url)
        data_fetcher = DataFetcher()
        data_saver = DataSaver('articles.json')

        # creating a DataProcessor instance and passing dependencies
        self.data_processor = DataProcessor(data_fetcher, data_saver)

    def get_title(self):
        return super().get_title()

    def get_element(self, by: str, value: str):
        return super().get_element(by, value)

    def fetch_data(self):
        # processing the relevant news_data using DataProcessor class.
        self.data_processor.process_news_data()


