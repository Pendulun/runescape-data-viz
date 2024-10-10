import pathlib


class Settings:
    PROJECT_NAME: str = "Runescape data viz"
    PROJECT_VERSION: str = "1.0.0"


class runescapeRoutesFormats:
    CATEGORY: str = "https://services.runescape.com/m=itemdb_rs/api/catalogue/category.json?category={}"
    INFO: str = "https://secure.runescape.com/m=itemdb_rs/api/info.json"
    CATEGORY_ITEMS: str = "https://services.runescape.com/m=itemdb_rs/api/catalogue/items.json?category={}&alpha={}&page={}"
    ITEM_INFO: str = "https://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item={}"
    ITEM_PRICES: str = "https://services.runescape.com/m=itemdb_rs/api/graph/{}.json"


class dataSettings:
    DATA_DIR_PATH: str = "./backend/data/"
    ITEMS_CLASSES_FILE_NAME: str = "items_classes.txt"

    LOG_DIR: str = "./log"
    LOG_DATE_FMT = LOG_DIR + "/{}_{}_{}/"

    MAX_THREADS = 4

    @classmethod
    def get_items_classes_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.DATA_DIR_PATH) / pathlib.Path(
            cls.ITEMS_CLASSES_FILE_NAME)
