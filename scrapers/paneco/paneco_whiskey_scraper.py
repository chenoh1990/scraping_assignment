from .paneco_scraper import PanecoScraper
from .paneco_data.paneco_data_fetcher import PanecoDataFetcher
from .paneco_data.paneco_data_saver import PanecoDataSaver
from .paneco_data.paneco_data_processor import PanecoDataProcessor
from selenium.webdriver.support.ui import WebDriverWait


class PanecoWhiskeyScraper(PanecoScraper):

    def __init__(self, url: str):
        super().__init__(url)
        self.data_fetcher = PanecoDataFetcher(self)
        self.data_saver = PanecoDataSaver("whiskey_data.json")
        self.data_processor = PanecoDataProcessor(self.data_fetcher, self.data_saver)

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
        """Gets the driver from the grandparent class."""
        return super(PanecoScraper, self).driver

    def scroll_until_all_loaded(self, class_name="amscroll-page", timeout=20):
        """
        Scrolls down until all elements with the specified class are loaded or the page reaches the bottom.
        Uses WebDriverWait to repeatedly scroll and check if the page height has stopped increasing.

        :param class_name: The class name of dynamically loaded elements.
        :param timeout: Maximum wait time in seconds.
        """
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver:
                                                      driver.execute_script(
                                                          "window.scrollTo(0, document.body.scrollHeight);") or
                                                      driver.execute_script("return document.body.scrollHeight") ==
                                                      driver.execute_script(
                                                          "return window.innerHeight + window.scrollY")
                                                      )

            print(f"all elements with class: {class_name} have been successfully loaded.")

        except Exception as e:
            print(f"error occurred while scrolling: {e}")

        # scroll_pause_time = 2
        # last_height = self.driver.execute_script("return document.body.scrollHeight")
        #
        # while True:
        #     # Scroll down
        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(scroll_pause_time)  # Allow time for new content to load
        #
        #     # Wait until new class_name  divs are present
        #     WebDriverWait(self.driver, timeout).until(
        #         ec.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        #     )
        #
        #     # Get new scroll height
        #     new_height = self.driver.execute_script("return document.body.scrollHeight")
        #
        #     # If the height didn't change, we've reached the bottom
        #     if new_height == last_height:
        #         break
        #
        #     last_height = new_height

    def fetch_data(self):

        # processing the relevant paneco data using PanecoDataProcessor class.
        self.data_processor.process_data()
