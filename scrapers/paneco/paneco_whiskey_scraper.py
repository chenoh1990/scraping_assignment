from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from .paneco_scraper import PanecoScraper
from .paneco_data.paneco_data_fetcher import PanecoDataFetcher
from .paneco_data.paneco_data_saver import PanecoDataSaver
from .paneco_data.paneco_data_processor import PanecoDataProcessor
from logger.scraper_logger import Logger
import time


class PanecoWhiskeyScraper(PanecoScraper):

    LOG_NAME = "PanecoWhiskeyScraper"
    LOG_FILE = "logs/paneco_whiskey_scraper.log"

    def __init__(self, url: str):
        super().__init__(url)

        self.logger = Logger.get_logger(self.LOG_NAME, self.LOG_FILE)

        self.data_fetcher = PanecoDataFetcher(self, self.logger)
        self.data_saver = PanecoDataSaver("whiskey_data.json", self.logger)
        self.data_processor = PanecoDataProcessor(self.data_fetcher, self.data_saver, self.logger)

    def get_product_name(self):
        """Extracts the product name."""
        pass

    def get_price(self):
        """Extracts the product price."""
        pass

    def in_stock(self):
        """Checks if the product is in stock."""
        pass

    def get_bottle_image(self):
        """get bottle image from website"""
        pass

    def get_driver(self):
        """gets the driver from the grandparent class."""
        return super(PanecoScraper, self).driver

    def scroll_until_all_loaded(self, class_name="amscroll-page", timeout=20, max_scrolls=60):
        """
        Scrolls down until all elements with the specified class are loaded or the page reaches the bottom.
        Uses WebDriverWait to repeatedly scroll and check if the page height has stopped increasing.

        :param max_scrolls: number of max scrolls.
        :param class_name: The class name of dynamically loaded elements.
        :param timeout: Maximum wait time in seconds.
        """
        try:
            scroll_attempts = 0
            last_item_count = 0

            while scroll_attempts < max_scrolls:
                # scrolling down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(3)
                current_item_count = len(self.driver.find_elements(By.CLASS_NAME, class_name))

                if current_item_count == last_item_count:
                    break

                last_item_count = current_item_count
                scroll_attempts += 1

            self.logger.info(f"Loaded {last_item_count} items with class '{class_name}'.")

        except Exception as e:
            self.logger.error(f"an error occurred while scrolling.: {e}")

        try:
            WebDriverWait(self.driver, timeout).until(lambda driver:
                                                      driver.execute_script(
                                                          "window.scrollTo(0, document.body.scrollHeight);") or
                                                      driver.execute_script("return document.body.scrollHeight") ==
                                                      driver.execute_script(
                                                          "return window.innerHeight + window.scrollY")
                                                      )

            self.logger.info(f"all elements with class: {class_name} have been successfully loaded.")

        except Exception as e:
            self.logger.error(f"error occurred while scrolling: {e}")

    def fetch_data(self):
        # processing the relevant paneco data using PanecoDataProcessor class.
        self.logger.info("start processing relevant paneco data using PanecoDataProcessor")
        self.data_processor.process_data()
