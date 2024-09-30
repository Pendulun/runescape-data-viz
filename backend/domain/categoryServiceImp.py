from domain.categoryService import ICategoryService
from domain.repository.categoryRepo import ICategoryRepo


#Domain class.
class CategoryServiceImp(ICategoryService):

    def __init__(self, repo: ICategoryRepo) -> None:
        super().__init__()
        self.repo: ICategoryRepo = repo

    def get_category_info(self, cat_name: str) -> dict | None:
        cat_id = self.repo.get_category_id(cat_name)
        if cat_id:
            return self.repo.get_category_info(cat_id)
        else:
            return None

    def get_category_items(self, cat_name: str) -> list[dict] | None:
        cat_id = self.repo.get_category_id(cat_name)
        if cat_id:
            return self.repo.get_category_items(cat_id)
        else:
            return None
