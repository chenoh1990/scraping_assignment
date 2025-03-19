from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class PanecoDataFetcher:
    def __init__(self, scraper, logger):
        self.scraper = scraper
        self.logger = logger

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

        # get bottle name.
        name = self.get_text_by_css(product, "strong.product-item-name a")

        # get regular price by fetch wrapper class.
        wrapper_element = product.find_element(By.CLASS_NAME, "price-wrapper")
        regular_price_element = wrapper_element.find_element(By.CLASS_NAME, "price")
        regular_price = regular_price_element.text.strip()

        discounted_price = "not exist"
        try:
            discount_wrapper = product.find_element(By.CLASS_NAME, "special-price")
            price_wrapper = discount_wrapper.find_element(By.CLASS_NAME, "price-wrapper")
            discounted_price = price_wrapper.find_element(By.CLASS_NAME, "price").text.strip()

        except Exception:
            pass

        volume = self.get_text_by_css(product, "span.unit")
        internal_link = self.get_link_by_tag_name(product)

        self.logger.info(f"all product: {name} data was successfully extracted.")
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
            # wait until you find this html class that contains a link to the image.
            image_element = WebDriverWait(self.scraper.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, "fotorama__stage__shaft"))
            )
            bottle_image = image_element.find_element(By.TAG_NAME, "img").get_attribute("src")

        except Exception as e:
            self.logger.error(f"error {product_url}: {e}")
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
        self.logger.info(f"all internal product data has been successfully extracted.")
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

        (WebDriverWait(self.scraper.driver, 20)
         .until(lambda d: d.execute_script("return document.readyState") == "complete"))

        # Ensure all products are loaded by waiting until the last product is visible
        WebDriverWait(self.scraper.driver, 10).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, "li.item.product"))
        )

        # Find all elements
        products = self.scraper.get_elements("css", "li.item.product")

        return [self.extract_product_data(product) for product in products]
