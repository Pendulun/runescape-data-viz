from core.config import dataSettings
from functools import lru_cache
import pathlib


class ItemsCategories():
    CLASSES: list[str] | None = None

    @classmethod
    @lru_cache(maxsize=10)
    def get_category_id(cls, category_name: str) -> int | None:
        categories = cls.get_categories_list(dataSettings.ITEMS_CLASSES_PATH)
        try:
            return categories.index(category_name.lower())
        except Exception as e:
            return None

    @classmethod
    def get_categories_list(cls, file_path: pathlib.Path) -> list[str]:
        if cls.CLASSES:
            return cls.CLASSES
        try:
            with open(file_path, 'r') as file:
                cls.CLASSES = [
                    line.strip().split(",")[1].lower() for line in file
                    if line.strip()
                ]
            return cls.CLASSES
        except Exception as e:
            raise RuntimeError(f"Error loading values: {e}")
