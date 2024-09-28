from repository.items_categories import ItemsCategories

from fastapi import APIRouter
import requests
from core.config import runescapeRoutesFormats

router = APIRouter()


@router.get("/{category_name}")
def category_info(category_name: str):
    cat_id = ItemsCategories.get_category_id(category_name)
    if cat_id:
        request_url = runescapeRoutesFormats.CATEGORY.format(cat_id)
        category_info = requests.get(request_url)
        data = category_info.json()
        return data
    else:
        return None


@router.get("/{category_name}/items")
def category_items(category_name: str):
    category_data = category_info(category_name)
    if category_data:
        return ItemsCategories.get_category_items(category_name,
                                                  category_data['alpha'])
    else:
        return None
