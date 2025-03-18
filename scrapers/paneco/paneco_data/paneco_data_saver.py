import json


class PanecoDataSaver:

    def __init__(self, file_name):
        self.file_name = file_name

    def save_data(self, products: list):

        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
