import logging


class LoggerWrapper():

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger

    def set_logger(self, logger: logging.Logger | None):
        self.logger = logger

    def warning(self, msg: str):
        if self.logger:
            self.logger.warning(msg)

    def info(self, msg: str):
        if self.logger:
            self.logger.info(msg)

    def debug(self, msg: str):
        if self.logger:
            self.logger.debug(msg)

    def error(self, msg: str):
        if self.logger:
            self.logger.error(msg)

    def exception(self, msg: str):
        if self.logger:
            self.logger.exception(msg)
