from scrapers.scraper_interface import SeleniumScraper
from abc import ABC, abstractmethod


class PanecoScraper(SeleniumScraper, ABC):

    def __init__(self, url: str):
        super().__init__(url)

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
