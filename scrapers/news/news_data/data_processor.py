from scrapers.news.news_data.data_fetcher import DataFetcher
from scrapers.news.news_data.data_saver import DataSaver
import re


class DataProcessor:
    """
    DataProcessor class manages the entire workflow of fetching, processing, and saving news data.

    this class uses DataFetcher to fetch articles from the API,
    and uses DataSaver to saves data in chunks to optimize performance.
    """
    def __init__(self, data_fetcher: DataFetcher, data_saver: DataSaver, logger):
        self.data_fetcher = data_fetcher
        self.data_saver = data_saver
        self.logger = logger

    def process_news_data(self):
        try:
            # get first page articles.
            response_data = self.data_fetcher.fetch_articles(
                api_url="https://www.gov.il/CollectorsWebApi/api/DataCollector/GetResults?CollectorType=news&&culture"
                        "=en")
            # save first page articles.
            if response_data:
                self.data_saver.save_data_in_chunks(response_data.get("results"))
                self.logger.info("articles in first page have been successfully saved.")

            # get all pages articles
            base_url = "https://www.gov.il/CollectorsWebApi/api/DataCollector/GetResults?CollectorType=news"

            # get all articles from paginated pages.
            paginated_articles = self.data_fetcher.fetch_paginated_articles(base_url, response_data.get('total'))

            # save the remaining articles in chunks of 50.
            if paginated_articles:
                self.data_saver.save_data_in_chunks(paginated_articles.get("results"), chunk_size=50)

        except Exception as ex:
            print(f"Error processing news data: {ex}")

    @staticmethod
    def remove_html_tags(html_content):
        """
        Removes HTML tags from the given content and returns the plain text.
        """
        clean_text = re.sub(r'<[^>]+>', '', html_content)  # Regular expression to remove HTML tags
        return clean_text
