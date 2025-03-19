from scrapers.scraper_interface import SeleniumScraper
from abc import ABC, abstractmethod
from logger.scraper_logger import Logger


class PanecoScraper(SeleniumScraper, ABC):
    """
       Abstract Scraper for Paneco website.
       this department provides a structure for building a scraper for each product department
        in the paneco store.
    """
    LOG_NAME = "PanecoScraper"
    LOG_FILE = "logs/paneco_scraper.log"

    def __init__(self, url: str):
        super().__init__(url)
        self.logger = Logger.get_logger(self.LOG_NAME, self.LOG_FILE)

    @abstractmethod
    def get_product_name(self):
        """Extracts the product name."""
        pass

    @abstractmethod
    def get_price(self):
        """Extracts the product price."""
        pass

    @abstractmethod
    def in_stock(self):
        """Checks if the product is in stock."""
        pass

    @abstractmethod
    def get_bottle_image(self):
        """get bottle image from website"""
        pass

    @abstractmethod
    def scroll_until_all_loaded(self, class_name,  timeout=20):
        pass

    def fetch_data(self):
        pass
