from datetime import datetime
from functools import lru_cache
import logging

from backend.domain.itemService import IItemService
from backend.domain.repository.itemRepo import IItemRepo
from backend.common.logger_wrapper import LoggerWrapper


class ItemServiceImp(IItemService):
    SINGLETON = None

    def __init__(self, repo: IItemRepo, logger: logging.Logger = None) -> None:
        if self.SINGLETON:
            return self.SINGLETON
        else:
            self.SINGLETON = super().__init__()
            self.repo = repo
            self.logger = LoggerWrapper(logger)

    def set_logger(self, logger: logging.Logger):
        self.logger.set_logger(logger)

    @lru_cache(maxsize=10)
    def get_item_info(self, item_id: int) -> dict:
        try:
            item_info = self.repo.get_item_info(item_id)
        except Exception as e:
            self.logger.exception(
                "ItemServiceImp - get_item_info: Exception Occured")
            return dict()
        else:
            if 'item' in item_info:
                return item_info['item']
            else:
                return item_info

    @lru_cache
    def get_item_prices(self, item_id: int) -> dict:
        try:
            item_prices = self.repo.get_item_prices(item_id)
        except Exception as e:
            self.logger.exception(
                "ItemServiceImp - get_item_prices: Exception Occured")
            return None
        else:
            formated_prices = dict()
            if item_prices:
                daily_prices = {
                    datetime.fromtimestamp(int(timestamp) / 1000).date(): price
                    for timestamp, price in item_prices['daily'].items()
                }

                average_prices = {
                    datetime.fromtimestamp(int(timestamp) / 1000).date(): price
                    for timestamp, price in item_prices['average'].items()
                }
                formated_prices['daily'] = daily_prices
                formated_prices['average'] = average_prices
            return formated_prices
