import abc

# Conceptually, in a Hexagonal Architecture, this interface is an exit port
class IRunescapeAPIInfoRepo(abc.ABC):

    #Must be a singleton
    _instance = None

    def __call__(self, *args, **kwds) -> "IRunescapeAPIInfoRepo":
        if not self._instance:
            self._instance = super().__call__(*args, **kwds)

        return self._instance

    @abc.abstractmethod
    def get_last_updated(self) -> int | None:
        return None