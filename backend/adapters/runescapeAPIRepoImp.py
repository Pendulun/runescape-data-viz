from functools import lru_cache
import logging
import requests

from backend.common.logger_wrapper import LoggerWrapper
from backend.core.config import runescapeRoutesFormats
from backend.domain.repository.runescapeAPIRepo import IRunescapeAPIInfoRepo


class RunescapeAPIInfoRepo(IRunescapeAPIInfoRepo):
    SINGLETON = None

    def __init__(self, logger: logging.Logger = None) -> None:
        if self.SINGLETON:
            return self.SINGLETON
        else:
            self.SINGLETON = super().__init__()
            self.classes = None
            self.logger = LoggerWrapper(logger)

    def set_logger(self, logger: logging.Logger):
        self.logger.set_logger(logger)

    def get_last_updated(self) -> int | None:
        try:
            data = requests.get(runescapeRoutesFormats.INFO)
        except Exception as e:
            self.logger.exception(
                "RunescapeAPIInfoRepo - get_last_updated: Exception caught!")
            raise e
        else:
            item_data = dict()
            if data:
                item_data = data.json()
                return int(item_data['lastConfigUpdateRuneday'])
            return None
