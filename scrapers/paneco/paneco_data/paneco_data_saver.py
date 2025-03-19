import json


class PanecoDataSaver:

    def __init__(self, file_name, logger):
        self.file_name = file_name
        self.logger = logger

    def save_data(self, products: list):
        """
         saves the information in a json file.
        :param products: list of bottles with relevant data.

        :return:
        """

        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

        self.logger.info(f"data saved successfully in {self.file_name}")
