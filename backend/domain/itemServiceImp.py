from domain.itemService import IItemService
from domain.repository.itemRepo import IItemRepo
from functools import lru_cache


class ItemServiceImp(IItemService):

    def __init__(self, repo: IItemRepo) -> None:
        super().__init__()
        self.repo = repo

    @lru_cache(maxsize=10)
    def get_item_info(self, item_id: int) -> dict:
        try:
            item_info = self.repo.get_item_info(item_id)
        except Exception as e:
            print(f"[LOG] Exception Occured: {e}")
            return None
        else:
            return item_info
