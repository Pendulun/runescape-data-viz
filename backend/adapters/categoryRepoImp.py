import pathlib
from functools import lru_cache
import requests

from core.config import dataSettings, runescapeRoutesFormats
from domain.repository.categoryRepo import ICategoryRepo


# This is an implementation of a Out port.
# That is, conceptually, in a Hexagonal Architecture, this is an Adapter
class CategoryRepoRequest(ICategoryRepo):

    def __init__(self) -> None:
        super().__init__()
        self.classes = None

    @lru_cache(maxsize=10)
    def get_category_id(self, category_name: str) -> int | None:
        categories = self.get_categories_list()
        try:
            return categories.index(category_name.lower())
        except Exception as e:
            print(f"[LOG] Exception occurred!: {e}")
            return None

    def get_categories_list(self) -> list[str] | None:
        if self.classes:
            return self.classes
        try:
            target_file_path = pathlib.Path(dataSettings.ITEMS_CLASSES_PATH)
            with open(target_file_path, 'r') as file:
                self.classes = [
                    line.strip().split(",")[1].lower() for line in file
                    if line.strip()
                ]
            return self.classes
        except Exception as e:
            raise RuntimeError(f"Error loading values: {e}")

    def get_category_info(self, cat_id: int) -> dict | None:
        print(f"[LOG] Entrou no CatRepoRequest")
        print(f"[LOG] Cat ID: {cat_id}")
        request_url = runescapeRoutesFormats.CATEGORY.format(cat_id)
        data = None
        try:
            category_info = requests.get(request_url)
            print(f"[LOG] Request status: {category_info.status_code}")
            print(f"[LOG] Category Info response: {category_info.json()}")
        except Exception as e:
            print(f"[LOG] Exception caught: {e}")
        else:
            if category_info:
                data = category_info.json()
        finally:
            return data

    def get_category_items(self, cat_id: int) -> list[dict] | None:
        category_data = self.get_category_info(cat_id)
        if category_data:
            items_per_first_letter = category_data['alpha']
            print(items_per_first_letter)

            letters_with_items = [
                letter_dict for letter_dict in items_per_first_letter
                if letter_dict['items'] > 0
            ]

            items = self._aggregate_cat_items(cat_id, letters_with_items)
            print(f"[LOG] N items total: {len(items)}")

            return items
        else:
            return None

    def _aggregate_cat_items(self, cat_id: int,
                             letters_and_n_items: list[dict]) -> list[dict]:
        items = list()
        #TODO paralelize this for
        for letter_dict in letters_and_n_items:
            letter_items = self._request_items_for_cat_and_letter(
                cat_id, letter_dict)
            items.extend(letter_items)
        return items

    def _request_items_for_cat_and_letter(self, cat_id:int, letter_dict:dict):
        letter_items = list()
        curr_page = 1
        letter, n_items_total = letter_dict['letter'], letter_dict['items']
        print(f"[LOG] CURR letter: {letter}, n_items: {n_items_total}")

        while n_items_total > 0:
            request_url = runescapeRoutesFormats.CATEGORY_ITEMS.format(
                cat_id, letter, curr_page)
            print(f"[LOG] request url: {request_url}")

            try:
                response = requests.get(request_url)
            except Exception as e:
                print(f"[LOG] An exception occurred: {e}")
                break
            else:
                if response:
                    curr_items_data = response.json()
                    letter_items.extend(curr_items_data['items'])
                    n_items_this_request = len(curr_items_data['items'])
                    curr_page += 1
                    print(
                        f"[LOG] N items this request: {n_items_this_request}")
                    n_items_total -= n_items_this_request
                    print(f"[LOG] N items left: {n_items_total}")
                else:
                    print(
                        f"[LOG] Request for {request_url} returned None! Breaking"
                    )
                    break
        return letter_items
