import pytest
import requests
from unittest.mock import patch, Mock
from data.data_fetcher import DataFetcher


def test_fetch_articles_success():
    """Test successful fetching of articles."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"results": [{"title": "Test Article"}]}

    with patch('requests.get', return_value=mock_response):
        result = DataFetcher.fetch_articles("http://test.com/api")
        assert result == {"results": [{"title": "Test Article"}]}


def test_fetch_articles_failure():
    """Test fetching articles with a failure status code."""
    mock_response = Mock()
    mock_response.status_code = 404

    with patch('requests.get', return_value=mock_response):
        result = DataFetcher.fetch_articles("http://test.com/api")
        assert result is None


def test_fetch_article_content_success():
    """Test successful fetching of article content."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"content": "Test Content"}

    with patch('requests.get', return_value=mock_response):
        result = DataFetcher.fetch_article_content("http://test.com/article/test-article")
        assert result == {"content": "Test Content"}


def test_fetch_article_content_failure():
    """Test fetching article content with a failure status code."""
    mock_response = Mock()
    mock_response.status_code = 404

    with patch('requests.get', return_value=mock_response):
        result = DataFetcher.fetch_article_content("http://test.com/article/test-article")
        assert result is None


def test_fetch_article_content_exception():
    """Test fetching article content with an exception."""
    with patch('requests.get', side_effect=requests.RequestException("Test Exception")):
        result = DataFetcher.fetch_article_content("http://test.com/article/test-article")
        assert result is None


def test_fetch_paginated_articles():
    """Test fetching paginated articles."""
    mock_response1 = Mock()
    mock_response1.status_code = 200
    mock_response1.json.return_value = {"results": [{"title": "Article 1"}]}

    mock_response2 = Mock()
    mock_response2.status_code = 200
    mock_response2.json.return_value = {"results": [{"title": "Article 2"}]}

    with patch('requests.get', side_effect=[mock_response1, mock_response2]):
        result = DataFetcher.fetch_paginated_articles("http://test.com/api", 20, interval=10)

        assert len(result['results']) == 1
        assert result['results'][0]['title'] == "Article 1"
        assert result['total'] == 20
