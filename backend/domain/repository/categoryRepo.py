import abc

# Conceptually, in a Hexagonal Architecture, this interface is an exit port
class ICategoryRepo(abc.ABC):

    #Must be a singleton
    _instance = None

    def __call__(self, *args, **kwds) -> "ICategoryRepo":
        if not self._instance:
            self._instance = super().__call__(*args, **kwds)

        return self._instance

    @abc.abstractmethod
    def get_category_id(self, cat_name: str) -> int | None:
        return None

    @abc.abstractmethod
    def get_categories_list(self) -> list[str] | None:
        return None

    @abc.abstractmethod
    def get_category_info(self, cat_id: int) -> dict | None:
        return None
    
    @abc.abstractmethod
    def get_category_items(self, cat_id: int) -> list[dict] | None:
        return None
