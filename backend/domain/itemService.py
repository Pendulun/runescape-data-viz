from abc import ABC, abstractmethod


class IItemService(ABC):

    @abstractmethod
    def get_item_info(self, item_id: int) -> dict:
        return None

    @abstractmethod
    def get_item_prices(self, item_id: int) -> dict:
        return None
