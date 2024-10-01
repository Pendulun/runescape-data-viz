import abc

# Conceptually, in a Hexagonal Architecture, this interface is an entry port
class ICategoryService(abc.ABC):
    @abc.abstractmethod
    def get_category_info(self, category_name:str) -> dict | None:
        return None
    
    @abc.abstractmethod
    def get_category_items(self, category_name:str) -> list[dict] | None:
        return None
    
    @abc.abstractmethod
    def get_categories(self) ->list[str] | None:
        return None