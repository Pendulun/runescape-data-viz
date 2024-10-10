import datetime
import logging

from backend.domain.runescapeAPIService import IRunescapeAPIInfo
from backend.domain.repository.runescapeAPIRepo import IRunescapeAPIInfoRepo
from backend.common.logger_wrapper import LoggerWrapper


class RunescapeAPIInfo(IRunescapeAPIInfo):
    SINGLETON = None

    def __init__(self,
                 repo: IRunescapeAPIInfoRepo,
                 logger: logging.Logger = None) -> None:
        if self.SINGLETON:
            return self.SINGLETON
        else:
            self.SINGLETON = super().__init__()
            self.repo = repo
            self.logger = LoggerWrapper(logger)

    def set_logger(self, logger: logging.Logger):
        self.logger.set_logger(logger)

    def get_last_updated(self) -> datetime.datetime:
        try:
            result = self.repo.get_last_updated()
        except Exception as e:
            self.logger.exception(
                "RunescapeAPIInfo - get_last_updated_info: Exception Occured")
            return dict()
        else:
            base_date = datetime.datetime(year=2002, month=2, day=27)
            date_updated = base_date + datetime.timedelta(days=int(result))
            return date_updated.date()
