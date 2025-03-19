from scrapers.news.gov_news_scraper import NewsSiteScraper
from scrapers.paneco.paneco_whiskey_scraper import PanecoWhiskeyScraper


class ScraperFactory:
    """
    factory class for creating different types of scrapers dynamically.

    provides a centralized way to instantiate scrapers based on
    the provided type and ensures that the correct scraper is initialized
    without requiring direct instantiation in the main application.

    """
    @staticmethod
    def create_scraper(scraper_type: str, url: str):
        """Creates a scraper instance based on the provided type."""

        # Scraper initializer for the NewsSiteScraper class.
        if scraper_type == "news":
            return NewsSiteScraper(url)

        # Scraper initializer for the PanecoWhiskeyScraper class.
        elif scraper_type == "paneco":
            return PanecoWhiskeyScraper(url)
        else:
            raise ValueError(f"Unknown scraper type: {scraper_type}")
