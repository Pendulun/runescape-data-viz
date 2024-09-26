from core.config import dataSettings
from functools import lru_cache

@lru_cache(maxsize=10)
def get_category_id(category_name:str) -> int | None:
    name_to_id_map = dict()
    with open(dataSettings.ITEMS_CLASSES_PATH, 'r') as file:
        line = file.readline().strip()
        while line:
            splitted_line = line.split(",")
            id = splitted_line[0]
            category = splitted_line[1].lower()
            name_to_id_map[category] = id
            line = file.readline().strip()
    
    return name_to_id_map.get(category_name, None)
    


