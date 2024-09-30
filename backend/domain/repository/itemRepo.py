import abc

# Conceptually, in a Hexagonal Architecture, this interface is an exit port
class IItemRepo(abc.ABC):

    #Must be a singleton
    _instance = None

    def __call__(self, *args, **kwds) -> "IItemRepo":
        if not self._instance:
            self._instance = super().__call__(*args, **kwds)

        return self._instance

    @abc.abstractmethod
    def get_item_info(self, item_id: int) -> int | None:
        return None