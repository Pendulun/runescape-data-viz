from functools import lru_cache
import requests

from core.config import runescapeRoutesFormats
from domain.repository.itemRepo import IItemRepo


# This is an implementation of a Out port.
# That is, conceptually, in a Hexagonal Architecture, this is an Adapter
class ItemRepoRequest(IItemRepo):

    def __init__(self) -> None:
        super().__init__()
        self.classes = None

    @lru_cache(maxsize=10)
    def get_item_info(self, item_id: int) -> dict | None:
        request_path = runescapeRoutesFormats.ITEM_INFO.format(item_id)
        try:
            data = requests.get(request_path)
        except Exception as e:
            print(f"[LOG] Exception caught! {e}")
            raise e
        else:
            item_data = dict()
            if data:
                item_data = data.json()
            return item_data

    @lru_cache(maxsize=10)
    def get_item_prices(self, item_id: int) -> dict | None:
        request_path = runescapeRoutesFormats.ITEM_PRICES.format(item_id)
        try:
            data = requests.get(request_path)
        except Exception as e:
            print(f"[LOG] Except caught! {e}")
            return None
        else:
            item_prices = None
            if data:
                item_prices = data.json()
            return item_prices
