import logging

from domain.categoryService import ICategoryService
from domain.repository.categoryRepo import ICategoryRepo
from common.logger_wrapper import LoggerWrapper


#Domain class.
class CategoryServiceImp(ICategoryService):

    def __init__(self, repo: ICategoryRepo, logger:logging.Logger=None) -> None:
        super().__init__()
        self.repo: ICategoryRepo = repo
        self.logger = LoggerWrapper(logger)
    
    def set_logger(self, logger:logging.Logger):
        self.logger.set_logger(logger)

    def get_category_info(self, cat_name: str) -> dict | None:
        cat_id = self.repo.get_category_id(cat_name)
        if cat_id:
            return self.repo.get_category_info(cat_id)
        else:
            return None

    def get_category_items(self, cat_name: str) -> list[dict] | None:
        cat_id = self.repo.get_category_id(cat_name)
        self.logger.debug(f"Category name: {cat_name}. Category id: {cat_id}")
        if cat_id is not None:
            self.logger.info(f"Searching for category {cat_id} items")
            return self.repo.get_category_items(cat_id)
        else:
            self.logger.warning(f"Category {cat_name} doesn't have an ID!")
            return None
    
    def get_categories(self) -> list[str] | None:
        return self.repo.get_categories_list()
