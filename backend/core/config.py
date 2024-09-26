import pathlib

class Settings:
    PROJECT_NAME:str = "Runescape data viz"
    PROJECT_VERSION: str = "1.0.0"

class runescapeRoutesFormats:
    CATEGORY:str = "https://services.runescape.com/m=itemdb_rs/api/catalogue/category.json?category={}"
    INFO:str = "https://secure.runescape.com/m=itemdb_rs/api/info.json"

class dataSettings:
    DATA_DIR_PATH:str = "./data/"
    ITEMS_CLASSES_PATH:str = pathlib.Path(DATA_DIR_PATH + "items_classes.txt")