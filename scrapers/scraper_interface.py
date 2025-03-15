from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import requests


class Scraper(ABC):
    """
    the Scraper interface defines a common structure for web scrapers, ensuring that different implementations follow
    a standardized approach.

    it provides abstract methods that must be implemented by any scraper,
    whether it uses requests for static pages or selenium for dynamic ones.
    """

    def __init__(self, url):
        self.session = self.create_session()
        self.url = url

    @abstractmethod
    def create_session(self):
        pass

    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def get_element(self, by: str, value: str):
        """Retrieve an element by a given selector and method."""
        pass


class SeleniumScraper(Scraper):
    """
    Scraper for dynamic websites using Selenium library.
    """

    def __init__(self, url: str):
        super().__init__(url)

    def create_session(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        return webdriver.Chrome(options=options)

    def get_title(self):
        self.session.get(self.url)
        return self.session.title

    def get_element(self, by, value):
        by_mapping = {
            "id": By.ID,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
        }
        return self.session.find_element(by_mapping[by], value)


class RequestsScraper(Scraper):
    """
    Scraper for static websites using the requests library without BeautifulSoup.
    """

    def __init__(self, url: str):
        super().__init__(url)
        self.url = url

    def create_session(self):
        return requests.Session()

    def get_title(self):
        response = self.session.get(self.url)
        response.raise_for_status()
        match = re.search(r"<title>(.*?)</title>", response.text, re.IGNORECASE)

        return match.group(1) if match else "No title found"

    def get_element(self, by: str, value: str):
        response = self.session.get(self.url)
        response.raise_for_status()

        if by == "id":
            pattern = rf'id="{value}"[^>]*>(.*?)</'
        elif by == "class":
            pattern = rf'class="{value}"[^>]*>(.*?)</'
        elif by == "tag":
            pattern = rf'<{value}[^>]*>(.*?)</{value}>'
        else:
            raise ValueError("Unsupported selector method.")

        match = re.search(pattern, response.text, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else "Element not found"
