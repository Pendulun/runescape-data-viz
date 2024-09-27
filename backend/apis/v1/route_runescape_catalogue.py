from repository.items_categories import ItemsCategories

from fastapi import APIRouter
import requests
from core.config import runescapeRoutesFormats

router = APIRouter()


@router.get("/{category_name}")
def catalogue(category_name: str):
    cat_id = ItemsCategories.get_category_id(category_name)
    if cat_id:
        request_url = runescapeRoutesFormats.CATEGORY.format(cat_id)
        category_info = requests.get(request_url)
        data = category_info.json()
        return data
    else:
        return None
