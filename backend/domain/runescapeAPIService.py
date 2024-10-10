from abc import ABC, abstractmethod
import datetime

class IRunescapeAPIInfo(ABC):

    @abstractmethod
    def get_last_updated(self) -> datetime:
        return None
