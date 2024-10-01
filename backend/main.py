import logging
from datetime import datetime
import pathlib

from adapters.apis.base import api_router
from adapters.server import ServerAdapters
from adapters.categoryRepoImp import CategoryRepoRequest
from domain.categoryServiceImp import CategoryServiceImp
from adapters.itemRepoImp import ItemRepoRequest
from domain.itemServiceImp import ItemServiceImp
from core.config import Settings, dataSettings

from fastapi import FastAPI


def set_up_logger() -> logging.Logger:
    curr_date = datetime.today().date()
    curr_date_log_dir = pathlib.Path(
        dataSettings.LOG_DATE_FMT.format(curr_date.year, curr_date.month,
                                         curr_date.day))
    curr_date_log_dir.mkdir(exist_ok=True, parents=True)

    logger = logging.getLogger(__name__)
    logger.setLevel("DEBUG")

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(
        f"log/{curr_date.year}_{curr_date.month}_{curr_date.day}/backend.log",
        mode="a",
        encoding="utf-8")
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    formatter = logging.Formatter("{asctime} - {levelname} - {message}",
                                  style="{",
                                  datefmt="%Y-%m-%d %H:%M")

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    console_handler.setLevel("DEBUG")
    file_handler.setLevel("INFO")
    return logger


logger = set_up_logger()

ServerAdapters.category_service = CategoryServiceImp(CategoryRepoRequest(logger), logger)
ServerAdapters.item_service = ItemServiceImp(ItemRepoRequest(logger), logger)

app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
app.include_router(api_router)
