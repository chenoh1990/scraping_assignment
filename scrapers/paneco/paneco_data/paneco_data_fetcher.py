from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class PanecoDataFetcher:
    def __init__(self, scraper):
        self.scraper = scraper

    @staticmethod
    def get_text_by_css(product, css_selector):
        """ returns text from a specific element """

        elements = product.find_elements(By.CSS_SELECTOR, css_selector)
        return elements[0].text.strip() if elements else "N/A"

    @staticmethod
    def get_link_by_tag_name(product):
        """returns the internal link of the product by finding the first <a> inside the product div. """
        try:
            return product.find_element(By.TAG_NAME, "a").get_attribute("href")

        except Exception as ex:
            print(f"failed to get internal link of product: {product}, error: {ex}")

    def extract_product_data(self, product):
        """ extracts data from a single product """

        name = self.get_text_by_css(product, "strong.product-item-name a")
        regular_price = self.get_text_by_css(product,
                                             "span.price-container .price-wrapper[paneco_data-price-type='finalPrice']")
        discounted_price = self.get_text_by_css(product,
                                                "span.price-container .price-wrapper["
                                                "paneco_data-price-type='registerPrice']")
        volume = self.get_text_by_css(product, "span.unit")
        internal_link = self.get_link_by_tag_name(product)

        return {
            "Name": name,
            "Regular Price": regular_price,
            "Discounted Price": discounted_price,
            "Volume": volume,
            "internal_link": internal_link
        }

    def fetch_internal_product_info(self, product_url):

        # open internal product page.
        self.scraper.driver.get(product_url)

        # get bottle image.
        WebDriverWait(self.scraper.driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "page-wrapper"))
        )
        try:
            image_element = WebDriverWait(self.scraper.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, "fotorama__stage__shaft"))
            )
            bottle_image = image_element.find_element(By.TAG_NAME, "img").get_attribute("src")

        except Exception as e:
            print(f"⚠️ error {product_url}: {e}")
            bottle_image = "N/A"

        description_elements = self.scraper.driver.find_elements(By.CSS_SELECTOR, "#description")
        if description_elements:
            description = description_elements[0].text.strip()
        else:
            description = "N/A"

        additional_data = {
            "description": description,
            "bottle_image": bottle_image,
        }

        return additional_data

    def fetch_data(self):
        """
        retrieves and extracts product data from the paneco web page.

        :return: list[dict]: A list of dictionaries, where each dictionary contains
                        the extracted product details (e.g., name, price, volume, link).
        """
        # handle pop up message
        self.scraper.handle_popup_message('css', "#dy-over-18yrs-popup")

        # scroll down page until all bottles appears in table.
        self.scraper.scroll_until_all_loaded(class_name="amscroll-page")
        (WebDriverWait(self.scraper.driver, 15)
         .until(lambda d: d.execute_script("return document.readyState") == "complete"))

        # Find all elements
        products = self.scraper.get_elements("css", "li.item.product")

        return [self.extract_product_data(product) for product in products]
