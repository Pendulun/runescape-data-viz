from domain.categoryService import ICategoryService
from domain.itemService import IItemService

class ServerAdapters():
    category_service: ICategoryService = None
    item_service: IItemService = None
