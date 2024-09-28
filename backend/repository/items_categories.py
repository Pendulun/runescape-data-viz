from functools import lru_cache
import pathlib
import requests

from core.config import dataSettings, runescapeRoutesFormats


class ItemsCategories():
    CLASSES: list[str] | None = None

    @classmethod
    @lru_cache(maxsize=10)
    def get_category_id(cls, category_name: str) -> int | None:
        categories = cls.get_categories_list(dataSettings.ITEMS_CLASSES_PATH)
        try:
            return categories.index(category_name.lower())
        except Exception as e:
            return None

    @classmethod
    def get_categories_list(cls, file_path: pathlib.Path) -> list[str]:
        if cls.CLASSES:
            return cls.CLASSES
        try:
            with open(file_path, 'r') as file:
                cls.CLASSES = [
                    line.strip().split(",")[1].lower() for line in file
                    if line.strip()
                ]
            return cls.CLASSES
        except Exception as e:
            raise RuntimeError(f"Error loading values: {e}")

    @classmethod
    def get_category_items(
            cls, category_name: str,
            items_per_first_letter: list[dict[str, int]]) -> list[dict]:
        category_id = ItemsCategories.get_category_id(category_name)
        print(items_per_first_letter)
        print(f"[LOG] Original n letters: {len(items_per_first_letter)}")
        letters_with_items = [
            letter_dict for letter_dict in items_per_first_letter
            if letter_dict['items'] > 0
        ]
        print(f"[LOG] N Letters with items: {len(letters_with_items)}")
        items = list()
        #TODO paralelize this for
        for letter_dict in letters_with_items:
            curr_page = 1
            letter, n_items_total = letter_dict['letter'], letter_dict['items']
            print(f"[LOG] CURR letter: {letter}, n_items: {n_items_total}")
            while n_items_total > 0:
                request_url = runescapeRoutesFormats.CATEGORY_ITEMS.format(
                    category_id, letter, curr_page)
                print(f"[LOG] request url: {request_url}")
                curr_items_data = requests.get(request_url).json()
                curr_page += 1
                items.extend(curr_items_data['items'])
                n_items_this_request = len(curr_items_data['items'])
                print(f"[LOG] N items this request: {n_items_this_request}")
                n_items_total -= n_items_this_request
                print(f"[LOG] N items left: {n_items_total}")

        print(f"[LOG] N items total: {len(items)}")
        return items
