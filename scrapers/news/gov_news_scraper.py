from scrapers.scraper_interface import SeleniumScraper
from scrapers.news.news_data.data_fetcher import DataFetcher
from scrapers.news.news_data.data_saver import DataSaver
from scrapers.news.news_data.data_processor import DataProcessor
from logger.scraper_logger import Logger


class NewsSiteScraper(SeleniumScraper):
    """
    NewsSiteScraper uses Selenium to scrape news_data from a news website.
    """
    LOG_NAME = "NewsSiteScraper"
    LOG_FILE = "logs/news_site_scraper.log"

    def __init__(self, url: str):
        super().__init__(url)
        # override the logger with a new instance for this class.
        self.logger = Logger.get_logger(self.LOG_NAME, self.LOG_FILE)
        data_fetcher = DataFetcher(self.logger)
        data_saver = DataSaver('articles.json', self.logger)

        # creating a DataProcessor instance and passing dependencies
        self.data_processor = DataProcessor(data_fetcher, data_saver, self.logger)

    def get_title(self):
        return super().get_title()

    def get_element(self, by: str, value: str):
        return super().get_element(by, value)

    def fetch_data(self):
        # processing the relevant news_data using DataProcessor class.
        self.logger.info("news scraper starts processing data from the site.")
        self.data_processor.process_news_data()
