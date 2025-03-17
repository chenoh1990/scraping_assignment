from data.data_fetcher import DataFetcher
from data.data_saver import DataSaver
import re


class DataProcessor:
    def __init__(self, data_fetcher: DataFetcher, data_saver: DataSaver):
        self.data_fetcher = data_fetcher
        self.data_saver = data_saver

    def process_news_data(self):
        try:
            # get first page articles.
            response_data = self.data_fetcher.fetch_articles(
                api_url="https://www.gov.il/CollectorsWebApi/api/DataCollector/GetResults?CollectorType=news&&culture=en")

            if response_data:
                self.data_saver.save_data_in_chunks(response_data.get("results"))

            # get all pages articles
            base_url = "https://www.gov.il/CollectorsWebApi/api/DataCollector/GetResults?CollectorType=news"

            # get all articles from paginated pages.
            remaining_articles = self.data_fetcher.fetch_paginated_articles(base_url, response_data.get('total'))

            if remaining_articles:
                self.data_saver.save_data_in_chunks(remaining_articles.get("results"), chunk_size=50)

        except Exception as ex:
            print(f"Error processing news data: {ex}")

    @staticmethod
    def remove_html_tags(html_content):
        """
        Removes HTML tags from the given content and returns the plain text.
        """
        clean_text = re.sub(r'<[^>]+>', '', html_content)  # Regular expression to remove HTML tags
        return clean_text
