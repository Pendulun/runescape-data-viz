from domain.repository.itemRepo import IItemRepo

class ItemRepoMock(IItemRepo):
    def get_item_info(self, item_id: int) -> dict | None:
        if not isinstance(item_id, int):
            return dict()
        return dict()
    
    def get_item_prices(self, item_id: int) -> dict | None:
        return super().get_item_prices(item_id)