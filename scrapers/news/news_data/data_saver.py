import json
from .data_fetcher import DataFetcher
from utils import remove_html_tags


class DataSaver:
    def __init__(self, file_name, logger):
        self.file_name = file_name
        self.logger = logger

    @staticmethod
    def extract_tags(tags):
        """
        extracting tags news_data from article.
        :param tags: a Dict of dictionaries.

        :return: organized dictionary for easy storage in a Json file.
        """
        tag_data = {}
        if 'metaData' in tags:
            for tag_name, tag_list in tags['metaData'].items():
                tag_data[tag_name] = [tag['title'] for tag in tag_list]

        if 'promotedMetaData' in tags:
            for tag_name, tag_list in tags['promotedMetaData'].items():
                tag_data[tag_name] = [tag['title'] for tag in tag_list]

        return tag_data

    def extract_section_data(self, article_content):
        """
        Extract the 'sectionData' from the article content.
        """
        try:
            section_data = article_content.get("contentMain", {}).get('htmlContents', [])[0].get('sectionData', None)

            # clean all HTML tags from content,
            clean_section_data = remove_html_tags(section_data)
            return clean_section_data

        except (IndexError, AttributeError) as e:
            self.logger.warning(f"Error extracting content from response: {e}")
            return None

    def load_existing_data(self):
        """Loads existing news_data from the JSON file."""
        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                return json.load(f)

        except FileNotFoundError:
            # If file doesn't exist, return an empty list
            self.logger.warning("file not exist, returns empty list.")
            return []

    def get_json_format_response(self, item: dict):
        article_response = DataFetcher.fetch_article_content(item.get("url"))

        if article_response is None:
            self.logger.error(f"No content in: {item.get('url')}")
            raise ValueError(f"No content returned for {item.get('url')}")

        article_content = DataSaver.extract_section_data(self, article_content=article_response)

        article = {
            'title': item['title'],
            'url': item['url'],
            'publish_date': item['tags']['metaData']['Publish Date'][0]['title'] if
            'Publish Date' in item['tags']['metaData'] else None,
            'description': item['description'],
            'tags': self.extract_tags(item['tags']),
            'article_content': article_content
        }
        return article

    def load_articles_from_file(self):
        """
        function checks if file already exist.
        if the file exist -> return list of all file news_data.
        if file not exist -> return empty list.
        """
        try:
            # Try to open the existing file to append news_data.
            with open(self.file_name, 'r', encoding='utf-8') as f:
                return json.load(f)

        except FileNotFoundError:
            # If file does not exist, start with an empty list.
            return []

    def extract_values_from_json(self, key: str = None):
        """
        Loads values from a JSON file and returns a list of existing values.

        If key is None, returns the entire list of dictionaries.

        :return: A list of existing values.
        """
        articles = self.load_articles_from_file()
        if key is None:
            return articles

        return [article[key] for article in articles]

    def save_data_in_chunks(self, data, chunk_size=100):
        """
        the function receives a list of articles and saves the relevant parameters in a json file.

        function steps:
            1. check of file already exist, if not exist, create new file.
            2. checks if urls exist to prevent double saving in the json file.
            3. save files in chunks to improve performance.

        :param data: A dictionary that contains a list of articles.
        :param chunk_size: 100 by default.
        :return:
        """
        # check if file exist.
        articles = self.load_articles_from_file()

        # create a list of existing URLs to prevent duplicates.
        existing_urls = [article['url'] for article in articles]

        # Save news_data in chunks to improve performance
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]

            for item in chunk:
                # checking if the article already exists by URL
                if item['url'] not in existing_urls:
                    try:
                        # get article in json format for easy save in json file.
                        article = self.get_json_format_response(item)

                        articles.append(article)
                        existing_urls.append(item['url'])

                    except ValueError as ex:
                        self.logger.error(f"Value error: {ex}")

                    except Exception as e:
                        self.logger.error(f"Error processing article {item.get('url')}: {e}")

            # Saving news_data to JSON file in chunks.
            with open(self.file_name, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=4)
                self.logger.info("news_data chunk saved successfully in json file.")
