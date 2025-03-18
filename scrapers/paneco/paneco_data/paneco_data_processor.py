from .paneco_data_fetcher import PanecoDataFetcher
from .paneco_data_saver import PanecoDataSaver


class PanecoDataProcessor:
    """
    This class manages the data processing flow for Paneco products.

    The class uses PanecoDataFetcher to fetch product data from the Paneco website,
    and uses PanecoDataSaver to save the processed data.
    """
    def __init__(self, paneco_data_fetcher: PanecoDataFetcher, paneco_data_saver: PanecoDataSaver):
        self.paneco_data_fetcher = paneco_data_fetcher
        self.paneco_data_saver = paneco_data_saver

    def process_data(self):
        """
        fetches product data, updates each product with additional internal information, and saves the data
        in chunks of 10 products at a time.

        ensures all products are saved, including any remaining ones at the end.
        """
        # get list of all bottles in paneco store section.
        products = self.paneco_data_fetcher.fetch_data()

        # update all products with internal information and save in chunks of 10 products each time.
        for index, product in enumerate(products):
            internal_info = self.paneco_data_fetcher.fetch_internal_product_info(product.get('internal_link'))

            if internal_info:
                product.update(internal_info)

            if (index + 1) % 10 == 0:
                self.paneco_data_saver.save_data(products[:index + 1])

        # saving all unsaved products if the total of all products is not divisible by 10.
        self.paneco_data_saver.save_data(products)
        return products
