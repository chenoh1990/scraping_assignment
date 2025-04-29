from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from logger.scraper_logger import Logger


class Scraper(ABC):
    """
    the Scraper interface defines a common structure for web scrapers, ensuring that different implementations follow
    a standardized approach.

    it provides abstract methods that must be implemented by any scraper,
    whether it uses requests for static pages or selenium for dynamic ones.
    """
    LOG_NAME = "BaseScraper"
    LOG_FILE = "logs/base_scraper.log"

    def __init__(self, url):
        self.session = None
        self.url = url
        self.logger = Logger.get_logger(self.LOG_NAME, self.LOG_FILE)

    @abstractmethod
    def create_driver(self):
        pass

    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def get_element(self, by: str, value: str):
        """Retrieve an element by a given selector and method."""
        pass

    @abstractmethod
    def close_driver(self):
        """Closes the WebDriver properly."""
        pass

    @abstractmethod
    def fetch_data(self):
        """fetch paneco_data from site"""
        pass


class SeleniumScraper(Scraper):
    """
    Scraper for dynamic websites using Selenium library.
    """
    LOG_NAME = "SeleniumScraper"
    LOG_FILE = "logs/selenium_scraper.log"

    def __init__(self, url: str, driver=None):
        super().__init__(url)
        self.driver = driver if driver else self.create_driver()
        self.logger = Logger.get_logger(self.LOG_NAME, self.LOG_FILE)

    def create_driver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--start-maximized")

        service = Service(ChromeDriverManager().install())
        try:
            driver = webdriver.Chrome(service=service, options=options)
            self.logger.info("driver initialized successfully.")
            return driver

        except Exception as e:
            self.logger.error(f"Failed to initialized WebDriver: {e}")
            raise

    def get_title(self):
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.TAG_NAME, "h1")))
            self.logger.info("website title successfully received.")
            return self.driver.title

        except Exception as e:
            self.logger.error(f"Error while waiting for title: {e}")
            return "No title found"

    def get_element(self, by, value):
        by_mapping = {
            "id": By.ID,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
        }
        try:
            return self.driver.find_element(by_mapping[by], value)

        except Exception as e:
            self.logger.error(f"failed to get elements,return empty list. error:{e}")
            return []

    def get_elements(self, by, value):
        by_mapping = {
            "id": By.ID,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
        }
        try:
            return self.driver.find_elements(by_mapping[by], value)

        except Exception as e:
            self.logger.error(f"failed to get elements,return None. error:{e}")
            return

    def close_driver(self):
        """Closes the WebDriver properly."""
        if self.driver:
            self.logger.info("driver closed")
            self.driver.quit()

    def handle_popup_message(self, by_type, popup_selector="#dy-over-18yrs-popup"):
        """
        Handles the popup if it appears on the site.
        :param by_type:
        :param popup_selector: CSS selector for the popup element.
        """
        try:
            element = self.get_element(by_type, popup_selector)
            element.click()
            self.logger.info("Popup closed successfully.")

        except Exception as ex:
            self.logger.error(f"No popup found or already closed, error: {ex}")

    def fetch_data(self):
        pass

    def scrape_site(self, url: str):
        # get url.
        self.driver.get(url)

        #
        self.fetch_data()

        # close browser.
        self.driver.quit()
