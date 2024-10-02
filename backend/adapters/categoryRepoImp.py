import concurrent.futures
from functools import lru_cache
import logging
import pathlib
import requests

from common.logger_wrapper import LoggerWrapper
from core.config import dataSettings, runescapeRoutesFormats
from domain.repository.categoryRepo import ICategoryRepo


# This is an implementation of a Out port.
# That is, conceptually, in a Hexagonal Architecture, this is an Adapter
class CategoryRepoRequest(ICategoryRepo):

    def __init__(self, logger: logging.Logger = None) -> None:
        super().__init__()
        self.classes = None
        self.logger = LoggerWrapper(logger)

    def set_logger(self, logger: logging.Logger):
        self.logger.set_logger(logger)

    @lru_cache(maxsize=10)
    def get_category_id(self, category_name: str) -> int | None:
        categories = self.get_categories_list()
        try:
            return categories.index(category_name.lower())
        except Exception as e:
            self.logger.exception(
                "CategoryRepoRequest - get_category_id: Exception Occured")
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
            self.logger.exception(
                "CategoryRepoRequest - get_categories_list: Error loading values"
            )

    def get_category_info(self, cat_id: int) -> dict | None:
        request_url = runescapeRoutesFormats.CATEGORY.format(cat_id)
        data = None
        try:
            category_info = requests.get(request_url)
        except Exception as e:
            self.logger.exception(
                "CategoryRepoRequest - get_category_info: Exception caught")
        else:
            if category_info:
                data = category_info.json()
        finally:
            return data

    def get_category_items(self, cat_id: int) -> list[dict] | None:
        category_data = self.get_category_info(cat_id)
        if category_data:
            items_per_first_letter = category_data['alpha']

            letters_with_items = [
                letter_dict for letter_dict in items_per_first_letter
                if letter_dict['items'] > 0
            ]
            self.logger.info(f"Retrieving category {cat_id} items")
            items = self._aggregate_cat_items(cat_id, letters_with_items)
            self.logger.debug(f"N items total: {len(items)}")

            return items
        else:
            return None

    def _aggregate_cat_items(self, cat_id: int,
                             letters_and_n_items: list[dict]) -> list[dict]:
        items = list()
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=dataSettings.MAX_THREADS) as executor:
            future_to_letter_dict = {
                executor.submit(self._request_items_for_cat_and_letter, cat_id, letter_dict):
                letter_dict
                for letter_dict in letters_and_n_items
            }
            for future in concurrent.futures.as_completed(
                    future_to_letter_dict):
                curr_letter_dict = future_to_letter_dict[future]
                try:
                    resultado = future.result()
                    items.extend(resultado)
                except Exception as exc:
                    self.logger.exception(
                        f'Request for {curr_letter_dict} generated an exception!'
                    )

            # for letter_dict in letters_and_n_items:
            #     letter_items = self._request_items_for_cat_and_letter(
            #         cat_id, letter_dict)
            #     items.extend(letter_items)
            items = sorted(items, key=lambda a: a['name'])
        return items

    def _request_items_for_cat_and_letter(self, cat_id: int,
                                          letter_dict: dict):
        letter_items = list()
        curr_page = 1
        letter, n_items_total = letter_dict['letter'], letter_dict['items']
        self.logger.debug(
            f"Cat_id: {cat_id}, letter: {letter}, n_items: {n_items_total}")

        while n_items_total > 0:
            request_url = runescapeRoutesFormats.CATEGORY_ITEMS.format(
                cat_id, letter, curr_page)
            self.logger.debug(f"Request url: {request_url}")
            try:
                response = requests.get(request_url)
            except Exception as e:
                self.logger.exception(
                    "CategoryRepoRequest - _request_items_for_cat_and_letter: Exception caught"
                )
                break
            else:
                if response:
                    curr_items_data = response.json()
                    letter_items.extend(curr_items_data['items'])
                    n_items_this_request = len(curr_items_data['items'])
                    curr_page += 1
                    self.logger.debug(
                        f"N items this request: {n_items_this_request}")
                    n_items_total -= n_items_this_request
                    self.logger.debug(f"N items left: {n_items_total}")
                else:
                    self.logger.warning(
                        f"Request for {request_url} returned None! Breaking")
                    break
        return letter_items
