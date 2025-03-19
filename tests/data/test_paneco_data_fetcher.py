import pytest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from scrapers.paneco.paneco_data.paneco_data_fetcher import PanecoDataFetcher


@pytest.fixture
def mock_scraper():
    """Creates a mock scraper with a mocked Selenium WebDriver."""
    scraper = MagicMock()
    scraper.driver = MagicMock()
    return scraper


@pytest.fixture
def mock_logger():
    """Creates a mock logger to avoid real logging during tests."""
    return MagicMock()


@pytest.fixture
def data_fetcher(mock_scraper, mock_logger):
    """creates an instance of PanecoDataFetcher with mocked dependencies."""
    return PanecoDataFetcher(scraper=mock_scraper, logger=mock_logger)


def test_get_text_by_css():
    """test extracting text from a specific element."""
    product = MagicMock()
    product.find_elements.return_value = [MagicMock(text="Test Product")]

    result = PanecoDataFetcher.get_text_by_css(product, "strong.product-item-name a")
    assert result == "Test Product"


def test_get_text_by_css_no_element():
    """Test when the CSS selector does not find any element."""
    product = MagicMock()
    product.find_elements.return_value = []

    result = PanecoDataFetcher.get_text_by_css(product, "strong.product-item-name a")
    assert result == "N/A"


def test_get_link_by_tag_name():
    """Test extracting internal link from product."""
    product = MagicMock()
    product.find_element.return_value.get_attribute.return_value = "https://example.com"

    result = PanecoDataFetcher.get_link_by_tag_name(product)
    assert result == "https://example.com"


def test_get_link_by_tag_name_fail():
    """Test when internal link extraction fails."""
    product = MagicMock()
    product.find_element.side_effect = Exception("Element not found")

    result = PanecoDataFetcher.get_link_by_tag_name(product)
    assert result is None


def test_extract_product_data(data_fetcher):
    """test extracting product data from a single product element."""
    product = MagicMock()
    product.find_element.side_effect = lambda by, value: MagicMock(text="100 ₪") if value == "price" else MagicMock()

    with patch.object(PanecoDataFetcher, "get_text_by_css", return_value="Test Whiskey"), \
         patch.object(PanecoDataFetcher, "get_link_by_tag_name", return_value="https://example.com"):

        result = data_fetcher.extract_product_data(product)

    assert result["Name"] == "Test Whiskey"
    assert result["internal_link"] == "https://example.com"


