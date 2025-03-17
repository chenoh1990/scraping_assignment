import json
import os
import pytest
from data.data_saver import DataSaver
from unittest.mock import patch, Mock


@pytest.fixture
def temp_json_file():
    """create a temporary JSON file for testing."""
    file_name = "temp_test_articles.json"
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump([], f)
    yield file_name

    os.remove(file_name)


@pytest.fixture
def data_saver(temp_json_file):
    """Fixture to create a DataSaver instance for testing."""
    return DataSaver(temp_json_file)


def test_load_existing_data_empty_file(data_saver, temp_json_file):
    """Test loading data from an empty file."""
    data = data_saver.load_existing_data()
    assert data == []


def test_load_existing_data_existing_data(data_saver, temp_json_file):
    """Test loading data from a file with existing data."""
    with open(temp_json_file, 'w', encoding='utf-8') as f:
        json.dump([{"title": "Existing Article"}], f)

    data = data_saver.load_existing_data()
    assert len(data) == 1
    assert data[0]['title'] == "Existing Article"


def test_extract_section_data():
    """Test extracting section data from article content."""
    article_content = {
        "contentMain": {
            "htmlContents": [
                {"sectionData": "<p>Test content</p>"}
            ]
        }
    }
    with patch('data.data_saver.remove_html_tags', return_value="Test content"):
        assert DataSaver.extract_section_data(article_content) == "Test content"


def test_extract_tags():
    """Test extracting tags from article data."""
    tags = {
        "metaData": {
            "category": [{"title": "Tech"}, {"title": "News"}],
            "author": [{"title": "John Doe"}]
        },
        "promotedMetaData": {
            "topic": [{"title": "AI"}]
        }
    }
    expected_tags = {
        "category": ["Tech", "News"],
        "author": ["John Doe"],
        "topic": ["AI"]
    }
    assert DataSaver.extract_tags(tags) == expected_tags


def test_get_json_format_response(data_saver, temp_json_file):
    """Test getting article in JSON format."""
    item = {
        "title": "Test Article",
        "url": "http://test.com/article",
        "tags": {
            "metaData": {"Publish Date": [{"title": "2023-10-26"}]}
        },
        "description": "Test description"
    }
    with patch('data.data_fetcher.DataFetcher.fetch_article_content') as mock_fetch:
        mock_fetch.return_value = {"contentMain": {"htmlContents": [{"sectionData": "<p>Content</p>"}]}}
        with patch('data.data_saver.remove_html_tags', return_value="Content"):
            article = data_saver.get_json_format_response(item)
            assert article["title"] == "Test Article"
            assert article["article_content"] == "Content"
