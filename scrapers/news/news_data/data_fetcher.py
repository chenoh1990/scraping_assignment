import requests
import concurrent.futures


class DataFetcher:
    """
       DataFetcher is responsible for fetching news_data from APIs.
    """

    @staticmethod
    def fetch_paginated_articles(base_url, total_articles, interval=10):
        """
        Fetch all articles from paginated API responses.
        :param total_articles:
        :param base_url: The base API URL for fetching articles.
        :param interval: The number of articles per request.

        :return: A list containing all articles.
        """
        articles = []

        current_page = 1
        pages_to_fetch = []

        while (current_page * interval) < total_articles:
            paginated_url = f"{base_url}&skip={(current_page * interval)}&culture=en"
            pages_to_fetch.append(paginated_url)
            current_page += 1

        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = list(executor.map(DataFetcher.fetch_articles, pages_to_fetch))

        for response in responses:
            if response:
                articles.extend(response.get('results', []))

        return {
            'total': total_articles,
            'results': articles
        }

    @staticmethod
    def fetch_articles(api_url: str, headers: dict = None):
        """
        Fetch news_data from the given API URL with optional headers.

        :param api_url: The URL of the API endpoint.
        :param headers: Optional headers to include in the request.
        :return: JSON news_data if the request is successful, None otherwise.
        """

        try:
            # Send the GET request using the requests library
            response = requests.get(api_url, headers=headers)

            # Check if the response status code is 200
            # if status code is 200 -> extract the article news_data from response.
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: Received status code {response.status_code}")
                return None

        except requests.RequestException as e:
            # handle any exceptions that occur during the request
            print(f"Request failed: {str(e)}")
            return None

    @staticmethod
    def fetch_article_content(article_url):
        """
        Fetch article content using the internal API URL.
        """
        article_name = article_url.split('/')[-1]  # Extract the article name from the URL.
        api_url = f"https://www.gov.il/ContentPageWebApi/api/content-pages/{article_name}?culture=en"

        try:
            # Fetch the content news_data using the API
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: Unable to fetch article content for {article_name}")
                return None

        except requests.RequestException as e:
            print(f"Error fetching article content: {e}")
            return None
