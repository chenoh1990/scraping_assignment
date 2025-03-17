from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Scraper(ABC):
    """
    the Scraper interface defines a common structure for web scrapers, ensuring that different implementations follow
    a standardized approach.

    it provides abstract methods that must be implemented by any scraper,
    whether it uses requests for static pages or selenium for dynamic ones.
    """

    def __init__(self, url):
        self.session = None
        self.url = url

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


class SeleniumScraper(Scraper):
    """
    Scraper for dynamic websites using Selenium library.
    """
    def __init__(self, url: str, driver=None):
        super().__init__(url)
        if driver:
            self.driver = driver
        else:
            self.driver = self.create_driver()

    def create_driver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")

        service = Service(ChromeDriverManager().install())
        try:
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception as e:
            print(f"Failed to start WebDriver: {e}")
            raise

    def get_title(self):
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.TAG_NAME, "h1")))
            return self.driver.title

        except Exception as e:
            print(f"Error while waiting for title: {e}")
            return "No title found"

    def get_element(self, by, value):
        by_mapping = {
            "id": By.ID,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
        }
        return self.driver.find_element(by_mapping[by], value)

    def close_driver(self):
        """Closes the WebDriver properly."""
        if self.driver:
            self.driver.quit()
